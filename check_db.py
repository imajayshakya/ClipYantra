import sqlite3
conn = sqlite3.connect('backend/alembic.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM alembic_version')
print('Alembic version:', cursor.fetchall())