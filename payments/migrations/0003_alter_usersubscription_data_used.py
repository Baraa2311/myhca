# Generated by Django 5.1.4 on 2025-01-02 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_plan_data_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='data_used',
            field=models.DecimalField(decimal_places=10, max_digits=20),
        ),
    ]
