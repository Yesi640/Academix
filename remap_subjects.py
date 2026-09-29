import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.subjects.models import Subject

# === Reasignar ARTE_DEPORTE a sus nuevas categorías ===
# Mapeo: nombre (partial) -> nueva categoría, is_primary
REMAP = {
    'Historia y Geografia': ('HISTORIA', True),
    'Ciencias Sociales':    ('HISTORIA', False),
    'Educacion Artistica':  ('ARTE', True),
    'Musica':               ('ARTE', False),
    'Educacion Fisica':     ('DEPORTE', True),
}

# Primero reasignar los que estaban en ARTE_DEPORTE
for subj in Subject.objects.filter(category='ARTE_DEPORTE'):
    matched = False
    for key, (new_cat, is_prim) in REMAP.items():
        if key.lower() in subj.name.lower():
            subj.category = new_cat
            subj.is_primary = is_prim
            subj.save()
            print(f"  ✔ {subj.name} -> {new_cat} (principal={is_prim})")
            matched = True
            break
    if not matched:
        # Por defecto asignar a ARTE si no coincide
        subj.category = 'ARTE'
        subj.is_primary = False
        subj.save()
        print(f"  ? {subj.name} -> ARTE (sin coincidencia exacta, revisar)")

# Reasignar Historia y Ciencias Sociales que estaban en PRINCIPAL
for subj in Subject.objects.filter(category='PRINCIPAL'):
    for key, (new_cat, is_prim) in REMAP.items():
        if key.lower() in subj.name.lower() and new_cat == 'HISTORIA':
            subj.category = 'HISTORIA'
            subj.is_primary = is_prim
            subj.save()
            print(f"  ✔ {subj.name} -> HISTORIA (principal={is_prim})")
            break

print("\n=== Estado final ===")
for cat in ['PRINCIPAL', 'HUMANISTICA', 'HISTORIA', 'ARTE', 'DEPORTE']:
    subjects = Subject.objects.filter(category=cat)
    print(f"\n[{cat}]")
    for s in subjects:
        marker = " ⭐ PRINCIPAL" if s.is_primary else ""
        print(f"  - {s.name}{marker}")
