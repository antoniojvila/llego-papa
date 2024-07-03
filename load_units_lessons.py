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
LESSONS_ROOT = os.path.join(settings.MEDIA_ROOT, 'LESSONS')
LESSONS_ICO_ROOT = os.path.join(settings.MEDIA_ROOT, 'LESSONS-ICO')

def get_level_and_name(folder_name):
    level, name = folder_name.split('-', 1)
    return int(level), name

def process_lessons(folder_path, unit):
    fs = FileSystemStorage()
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            name, extension = os.path.splitext(file_name)
            if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                # Mover la imagen a la carpeta correcta
                new_image_path = os.path.join('images', unit.name, file_name)
                new_image_full_path = os.path.join(settings.MEDIA_ROOT, new_image_path)

                # Crear directorio si no existe
                os.makedirs(os.path.dirname(new_image_full_path), exist_ok=True)

                # Mover el archivo
                with open(file_path, 'rb') as image_file:
                    fs.save(new_image_path, File(image_file))

                # Crear una lección
                lesson = Lessons(
                    name=name,
                    image=new_image_path,  # Guardar la ruta relativa en la base de datos
                    unit=unit
                )

                # Verificar si existe un video con el mismo nombre
                video_path = os.path.join(folder_path, f"{name}.mp4")
                if os.path.isfile(video_path):
                    new_video_path = os.path.join('videos', unit.name, f"{name}.mp4")
                    new_video_full_path = os.path.join(settings.MEDIA_ROOT, new_video_path)
                    os.makedirs(os.path.dirname(new_video_full_path), exist_ok=True)
                    with open(video_path, 'rb') as video_file:
                        fs.save(new_video_path, File(video_file))
                    lesson.video = new_video_path
                
                lesson.save()
                print(f'Lección creada: {name} en unidad: {unit.name}')

def assign_ico(folder_path, unit):
    fs = FileSystemStorage()
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            name, extension = os.path.splitext(file_name)
            if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                try:
                    lesson = Lessons.objects.get(name=name, unit=unit)
                    new_ico_path = os.path.join('images', unit.name, 'ico', file_name)
                    new_ico_full_path = os.path.join(settings.MEDIA_ROOT, new_ico_path)

                    # Crear directorio si no existe
                    os.makedirs(os.path.dirname(new_ico_full_path), exist_ok=True)

                    # Mover el archivo
                    with open(file_path, 'rb') as ico_file:
                        fs.save(new_ico_path, File(ico_file))

                    lesson.ico = new_ico_path
                    lesson.save()
                    print(f'Ícono asignado a lección: {name} en unidad: {unit.name}')
                except Lessons.DoesNotExist:
                    print(f'Lección no encontrada: {name} en unidad: {unit.name}')

def create_units_and_lessons():
    for folder_name in os.listdir(LESSONS_ROOT):
        folder_path = os.path.join(LESSONS_ROOT, folder_name)
        if os.path.isdir(folder_path):
            level, unit_name = get_level_and_name(folder_name)
            unit, created = Unit.objects.get_or_create(name=unit_name, level=level)
            process_lessons(folder_path, unit)
    
    for folder_name in os.listdir(LESSONS_ICO_ROOT):
        folder_path = os.path.join(LESSONS_ICO_ROOT, folder_name)
        if os.path.isdir(folder_path):
            level, unit_name = get_level_and_name(folder_name)
            try:
                unit = Unit.objects.get(name=unit_name, level=level)
                assign_ico(folder_path, unit)
            except Unit.DoesNotExist:
                print(f'Unidad no encontrada: {unit_name} con nivel: {level}')

if __name__ == '__main__':
    create_units_and_lessons()
