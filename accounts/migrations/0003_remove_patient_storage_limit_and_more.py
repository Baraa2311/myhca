# Generated by Django 5.1.4 on 2025-01-02 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_delete_administrator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='storage_limit',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='used_storage',
        ),
    ]
