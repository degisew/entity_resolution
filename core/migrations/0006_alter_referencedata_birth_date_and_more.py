# Generated by Django 4.2.6 on 2023-10-31 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_sourcedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencedata',
            name='birth_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sourcedata',
            name='birth_date',
            field=models.DateField(),
        ),
    ]
