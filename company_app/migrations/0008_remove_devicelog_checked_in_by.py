# Generated by Django 4.2.3 on 2023-08-27 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0007_alter_devicelog_checked_in_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicelog',
            name='checked_in_by',
        ),
    ]