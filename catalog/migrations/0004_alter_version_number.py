# Generated by Django 4.2.7 on 2023-12-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_version_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='number',
            field=models.CharField(max_length=8, verbose_name='Номер версии'),
        ),
    ]
