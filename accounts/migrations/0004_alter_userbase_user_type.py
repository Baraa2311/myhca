# Generated by Django 4.2.17 on 2025-01-07 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_patient_storage_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='user_type',
            field=models.CharField(choices=[('ADMIN', 'admin'), ('DOCTOR', 'doctor'), ('PATIENT', 'patient')], max_length=10),
        ),
    ]
