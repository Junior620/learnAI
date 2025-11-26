"""Vérifier l'état de l'import"""
import os
import psycopg2
from dotenv import load_dotenv

# Charger le .env du dossier backend
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from config import Config

conn = psycopg2.connect(
    host=Config.DB_HOST,
    database=Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    port=Config.DB_PORT
)
cur = conn.cursor()

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

print("📊 État de l'import sur Render:\n")
total = 0
for table in tables:
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    total += count
    status = "✅" if count > 0 else "⚪"
    print(f"{status} {table:25} {count:>10,} lignes")

print(f"\n{'='*40}")
print(f"📊 TOTAL: {total:,} lignes importées")
print(f"{'='*40}")

conn.close()
