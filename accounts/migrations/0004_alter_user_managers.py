# Generated by Django 5.0.7 on 2024-09-30 13:49

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_create_admin_account'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
