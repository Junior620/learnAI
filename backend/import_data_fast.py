"""
Script d'import rapide utilisant COPY pour PostgreSQL
Beaucoup plus rapide que INSERT pour les gros volumes
"""
import json
import psycopg2
from psycopg2 import sql
from io import StringIO
import csv
from config import Config

def import_table_fast(cursor, table_info, conn):
    """Importer les données d'une table avec COPY (ultra rapide)"""
    table_name = table_info['table']
    columns = table_info['columns']
    data = table_info['data']
    
    if not data:
        print(f"   ⚠️  {table_name}: Aucune donnée à importer")
        return 0
    
    try:
        # Pour la table grades, utiliser une table temporaire pour gérer les doublons
        if table_name == 'grades':
            temp_table = f"{table_name}_temp"
            
            # Créer table temporaire SANS les contraintes
            cursor.execute(f"CREATE TEMP TABLE {temp_table} (LIKE {table_name} INCLUDING DEFAULTS)")
            
            # Créer buffer CSV
            buffer = StringIO()
            writer = csv.writer(buffer, delimiter='\t')
            
            for row in data:
                row_values = [row.get(col) for col in columns]
                row_values = [r'\N' if v is None else str(v) for v in row_values]
                writer.writerow(row_values)
            
            buffer.seek(0)
            
            # Importer dans la table temporaire
            cols = ', '.join(columns)
            cursor.copy_expert(
                f"COPY {temp_table} ({cols}) FROM STDIN WITH (FORMAT CSV, DELIMITER E'\\t', NULL '\\N')",
                buffer
            )
            
            # Insérer depuis temp vers la vraie table en ignorant les doublons
            cursor.execute(f"""
                INSERT INTO {table_name} 
                SELECT * FROM {temp_table}
                ON CONFLICT DO NOTHING
            """)
            
            # Compter les lignes insérées
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            return count
        else:
            # Pour les autres tables, import direct
            buffer = StringIO()
            writer = csv.writer(buffer, delimiter='\t')
            
            for row in data:
                row_values = [row.get(col) for col in columns]
                row_values = [r'\N' if v is None else str(v) for v in row_values]
                writer.writerow(row_values)
            
            buffer.seek(0)
            
            cols = ', '.join(columns)
            cursor.copy_expert(
                f"COPY {table_name} ({cols}) FROM STDIN WITH (FORMAT CSV, DELIMITER E'\\t', NULL '\\N')",
                buffer
            )
            
            return len(data)
        
    except Exception as e:
        print(f"   ❌ Erreur import {table_name}: {e}")
        return 0

def import_all_data_fast(json_file='database_export.json'):
    """Importer toutes les données rapidement"""
    print("🚀 Import RAPIDE des données vers la base de production...\n")
    
    # Vérifier la configuration
    if not all([Config.DB_HOST, Config.DB_NAME, Config.DB_USER, Config.DB_PASSWORD]):
        print("❌ Variables de base de données non configurées!")
        return False
    
    # Lire le fichier JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            export_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {json_file} non trouvé!")
        return False
    
    # Connexion à la base de production
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = conn.cursor()
        
        print(f"✅ Connecté à {Config.DB_HOST}")
        print(f"📅 Export du: {export_data['export_date']}")
        print(f"📊 Tables à importer: {len(export_data['tables'])}\n")
        
        total_imported = 0
        
        # Ordre des tables (dépendances)
        table_order = [
            'users',
            'student_profiles',
            'subjects',
            'grades',
            'resources',
            'recommendations',
            'predictions',
            'chatbot_conversations',
            'alerts',
            'notifications'
        ]
        
        for table_name in table_order:
            if table_name in export_data['tables']:
                table_info = export_data['tables'][table_name]
                count = table_info['count']
                
                print(f"📊 Import de {table_name} ({count:,} lignes)...")
                
                imported = import_table_fast(cursor, table_info, conn)
                total_imported += imported
                
                # Commit après chaque table
                conn.commit()
                print(f"   ✅ {imported:,} lignes importées et sauvegardées\n")
        
        # Mettre à jour les séquences
        print("🔄 Mise à jour des séquences...")
        for table_name in table_order:
            try:
                cursor.execute(f"""
                    SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), 
                    COALESCE((SELECT MAX(id) FROM {table_name}), 1), true);
                """)
            except:
                pass
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n{'='*50}")
        print(f"✅ Import terminé avec succès!")
        print(f"📊 Total: {total_imported:,} lignes importées")
        print(f"{'='*50}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    import_all_data_fast()
