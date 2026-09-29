import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM pragma_table_info('courses_institutionsetting')")
cols = [r[0] for r in cursor.fetchall()]
print("Columnas actuales:", cols)

missing = ['logo', 'primary_color', 'secondary_color', 'hero_image', 'contact_email', 'contact_phone', 'website_url']
for col in missing:
    if col not in cols:
        print(f"FALTA: {col}")
        if col == 'logo':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN logo varchar(100) NULL DEFAULT ''")
        elif col == 'primary_color':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN primary_color varchar(7) NOT NULL DEFAULT '#7c3aed'")
        elif col == 'secondary_color':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN secondary_color varchar(7) NOT NULL DEFAULT '#c4b5fd'")
        elif col == 'hero_image':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN hero_image varchar(100) NULL DEFAULT ''")
        elif col == 'contact_email':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN contact_email varchar(254) NOT NULL DEFAULT ''")
        elif col == 'contact_phone':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN contact_phone varchar(30) NOT NULL DEFAULT ''")
        elif col == 'website_url':
            cursor.execute("ALTER TABLE courses_institutionsetting ADD COLUMN website_url varchar(200) NOT NULL DEFAULT ''")
        print(f"  -> Columna '{col}' agregada.")
    else:
        print(f"OK: {col}")

connection.commit()
print("Listo.")
