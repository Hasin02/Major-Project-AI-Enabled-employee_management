# Generated by Django 2.2.13 on 2024-04-07 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0007_auto_20240407_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp602', max_length=70),
        ),
    ]
