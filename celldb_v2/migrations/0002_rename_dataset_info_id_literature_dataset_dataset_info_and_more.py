# Generated by Django 4.2.2 on 2023-07-25 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celldb_v2', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='literature_dataset',
            old_name='dataset_info_id',
            new_name='dataset_info',
        ),
        migrations.RenameField(
            model_name='literature_dataset',
            old_name='literature_info_id',
            new_name='literature_info',
        ),
    ]