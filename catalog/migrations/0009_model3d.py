from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_product_ai_prompt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model3D',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Например: Кролик · фарфор', max_length=200, verbose_name='Название модели')),
                ('headline', models.CharField(blank=True, help_text='Если пусто — будет использовано название', max_length=200, verbose_name='Заголовок для витрины')),
                ('description', models.TextField(blank=True, help_text='Текст рядом с моделью на главной', verbose_name='Краткое описание')),
                ('glb_file', models.FileField(help_text='Бинарный glTF (.glb) — самый удобный формат', upload_to='models3d/', verbose_name='Файл .glb / .gltf')),
                ('poster', models.ImageField(blank=True, help_text='Картинка-заглушка, пока модель грузится. Можно оставить пустым.', null=True, upload_to='models3d/posters/', verbose_name='Постер (превью)')),
                ('auto_rotate', models.BooleanField(default=True, help_text='Модель плавно крутится сама', verbose_name='Авто-вращение')),
                ('rotation_speed', models.PositiveIntegerField(default=12, help_text='Рекомендуется 8–20', verbose_name='Скорость вращения (град/сек)')),
                ('camera_orbit', models.CharField(default='0deg 80deg 105%', help_text="Формат model-viewer: '0deg 75deg 105%' (азимут, наклон, радиус)", max_length=80, verbose_name='Стартовая орбита камеры')),
                ('exposure', models.FloatField(default=0.95, help_text='0.5 — темнее, 1.5 — ярче', verbose_name='Экспозиция')),
                ('is_active', models.BooleanField(default=True, help_text='Показывать на сайте', verbose_name='Активна')),
                ('order', models.PositiveIntegerField(default=0, help_text='Меньше — выше. Главная показывает первую активную.', verbose_name='Порядок')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '3D-модель',
                'verbose_name_plural': '3D-модели',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
