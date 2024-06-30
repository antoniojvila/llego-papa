import os
import django
from django.conf import settings

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from apps.signals.models import Unit, Lessons

# Ruta de la carpeta media
UNITS_ROOT = os.path.join(settings.MEDIA_ROOT, 'units')

def create_units_and_lessons():
    for folder_name in os.listdir(UNITS_ROOT):
        folder_path = os.path.join(UNITS_ROOT, folder_name)
        if os.path.isdir(folder_path):
            # Crear una unidad
            unit, created = Unit.objects.get_or_create(name=folder_name)
            
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    name, extension = os.path.splitext(file_name)
                    if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                        # Crear una lección
                        lesson = Lessons(
                            name=name,
                            image=os.path.join(folder_name, file_name),
                            unit=unit
                        )
                        lesson.save()
                        print(f'Lección creada: {name} en unidad: {folder_name}')

if __name__ == '__main__':
    create_units_and_lessons()
