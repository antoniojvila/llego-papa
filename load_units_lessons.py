import os
import django
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

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
                        # Mover la imagen a la carpeta correcta
                        new_image_path = os.path.join('images', folder_name, file_name)
                        new_image_full_path = os.path.join(settings.MEDIA_ROOT, new_image_path)

                        # Crear directorio si no existe
                        os.makedirs(os.path.dirname(new_image_full_path), exist_ok=True)

                        # Mover el archivo
                        fs = FileSystemStorage()
                        with open(file_path, 'rb') as image_file:
                            fs.save(new_image_path, File(image_file))

                        # Crear una lección
                        lesson = Lessons(
                            name=name,
                            image=new_image_path,  # Guardar la ruta relativa en la base de datos
                            unit=unit
                        )
                        lesson.save()
                        print(f'Lección creada: {name} en unidad: {folder_name}')

if __name__ == '__main__':
    create_units_and_lessons()
