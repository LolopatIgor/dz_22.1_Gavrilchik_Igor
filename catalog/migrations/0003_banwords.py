# Generated by Django 5.1.1 on 2024-10-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_product_manufactured_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='BanWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Слово')),
            ],
            options={
                'verbose_name': 'Запрещенное слово',
                'verbose_name_plural': 'Запрещенные слова',
            },
        ),
    ]
