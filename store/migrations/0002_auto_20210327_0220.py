# Generated by Django 3.1.5 on 2021-03-26 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ideal_for',
            new_name='gender',
        ),
    ]
