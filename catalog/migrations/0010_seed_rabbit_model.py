"""
Data-миграция: если в media/models3d/ уже лежит Rabbit.glb (положили вручную при первой раскатке),
создаём для него запись Model3D. Иначе — мягко пропускаем.
"""
import os
import shutil
from django.conf import settings
from django.db import migrations


GLB_FILENAME = 'Rabbit.glb'
TARGET_REL = f'models3d/{GLB_FILENAME}'


def seed_rabbit(apps, schema_editor):
    Model3D = apps.get_model('catalog', 'Model3D')

    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        return

    target_path = os.path.join(str(media_root), 'models3d', GLB_FILENAME)
    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir, exist_ok=True)

    # Если в media уже нет файла — попробуем поднять из корня проекта.
    if not os.path.exists(target_path):
        fallback = os.path.join(str(settings.BASE_DIR), GLB_FILENAME)
        if os.path.exists(fallback):
            try:
                shutil.copy2(fallback, target_path)
            except OSError:
                # не критично — просто не создадим запись
                return
        else:
            return

    # Не плодим дубликаты
    if Model3D.objects.filter(glb_file=TARGET_REL).exists():
        return

    Model3D.objects.create(
        name='Кролик · скульптурная композиция',
        headline='Объект в фокусе',
        description=(
            'Покрутите композицию и рассмотрите её со всех сторон. '
            'Так мы показываем фактуру, пропорции и пластику объекта — то, что не видно на статичном фото.'
        ),
        glb_file=TARGET_REL,
        auto_rotate=True,
        rotation_speed=10,
        camera_orbit='0deg 80deg 105%',
        exposure=0.95,
        is_active=True,
        order=0,
    )


def unseed_rabbit(apps, schema_editor):
    Model3D = apps.get_model('catalog', 'Model3D')
    Model3D.objects.filter(glb_file=TARGET_REL).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_model3d'),
    ]

    operations = [
        migrations.RunPython(seed_rabbit, reverse_code=unseed_rabbit),
    ]
