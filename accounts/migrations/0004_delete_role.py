# Generated by Django 4.0.4 on 2022-06-09 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
    ]