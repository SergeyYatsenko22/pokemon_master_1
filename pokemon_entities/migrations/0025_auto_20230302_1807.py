# Generated by Django 3.1.14 on 2023-03-02 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0024_auto_20230302_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(default='media/pokemon_images/No.jpg', upload_to='pokemon_images'),
        ),
    ]