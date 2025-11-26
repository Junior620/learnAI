"""
Script pour exporter les données de la base de données locale
"""
import psycopg2
import json
from datetime import datetime

# Configuration de ta base de données LOCALE
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'database': 'learnai',
    'user': 'postgres',
    'password': 'kidjamo@',  # Ton mot de passe local
    'port': 5432
}

def export_table_data(cursor, table_name):
    """Exporter les données d'une table"""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Convertir les types non-JSON en string
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, (list, dict)):
                    value = json.dumps(value)
                row_dict[col] = value
            data.append(row_dict)
        
        return {
            'table': table_name,
            'columns': columns,
            'data': data,
            'count': len(data)
        }
    except Exception as e:
        print(f"❌ Erreur export {table_name}: {e}")
        return None

def export_all_data():
    """Exporter toutes les données"""
    print("🔄 Connexion à la base de données locale...")
    
    try:
        conn = psycopg2.connect(**LOCAL_DB_CONFIG)
        cursor = conn.cursor()
        
        # Liste des tables à exporter (dans l'ordre des dépendances)
        tables = [
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
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'database': 'learnai',
            'tables': {}
        }
        
        total_rows = 0
        for table in tables:
            print(f"📊 Export de {table}...")
            table_data = export_table_data(cursor, table)
            if table_data:
                export_data['tables'][table] = table_data
                total_rows += table_data['count']
                print(f"   ✅ {table_data['count']} lignes exportées")
        
        cursor.close()
        conn.close()
        
        # Sauvegarder dans un fichier JSON
        output_file = 'database_export.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Export terminé!")
        print(f"📁 Fichier: {output_file}")
        print(f"📊 Total: {total_rows} lignes exportées")
        print(f"📋 Tables: {len(export_data['tables'])}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    export_all_data()
