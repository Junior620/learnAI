"""
Script pour importer les données exportées vers la base de données de production
"""
import json
import psycopg2
from psycopg2 import sql
from config import Config

def import_table_data(cursor, table_info):
    """Importer les données d'une table"""
    table_name = table_info['table']
    columns = table_info['columns']
    data = table_info['data']
    
    if not data:
        print(f"   ⚠️  {table_name}: Aucune donnée à importer")
        return 0
    
    try:
        # Construire la requête INSERT
        cols = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        
        # Préparer les données
        rows_to_insert = []
        for row in data:
            row_values = [row.get(col) for col in columns]
            rows_to_insert.append(tuple(row_values))
        
        # Insérer par batch de 1000 lignes pour plus de rapidité
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(rows_to_insert), batch_size):
            batch = rows_to_insert[i:i + batch_size]
            cursor.executemany(query, batch)
            total_inserted += len(batch)
            
            # Afficher la progression
            if total_inserted % 10000 == 0:
                print(f"      {total_inserted:,} / {len(rows_to_insert):,} lignes...")
        
        return len(rows_to_insert)
        
    except Exception as e:
        print(f"   ❌ Erreur import {table_name}: {e}")
        return 0

def import_all_data(json_file='database_export.json'):
    """Importer toutes les données depuis le fichier JSON"""
    print("🔄 Import des données vers la base de production...")
    
    # Vérifier la configuration
    if not all([Config.DB_HOST, Config.DB_NAME, Config.DB_USER, Config.DB_PASSWORD]):
        print("❌ Variables de base de données non configurées!")
        print("   Configure DB_HOST, DB_NAME, DB_USER, DB_PASSWORD sur Render")
        return False
    
    # Lire le fichier JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            export_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {json_file} non trouvé!")
        print("   Exécute d'abord: python backend/export_data.py")
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
        
        # Importer dans l'ordre des dépendances
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
                print(f"📊 Import de {table_name}...")
                table_info = export_data['tables'][table_name]
                count = import_table_data(cursor, table_info)
                total_imported += count
                print(f"   ✅ {count:,} lignes importées")
                
                # Commit après chaque table pour sauvegarder la progression
                conn.commit()
                print(f"   💾 Sauvegardé")
        
        # Mettre à jour les séquences (pour les ID auto-incrémentés)
        print("\n🔄 Mise à jour des séquences...")
        for table_name in table_order:
            try:
                cursor.execute(f"""
                    SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), 
                    COALESCE((SELECT MAX(id) FROM {table_name}), 1), true);
                """)
            except:
                pass  # Certaines tables n'ont pas de séquence
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✅ Import terminé!")
        print(f"📊 Total: {total_imported} lignes importées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    import_all_data()
