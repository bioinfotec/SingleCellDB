# Generated by Django 4.2.1 on 2023-06-24 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("celldb", "0003_tranmeta_delete_stuinfo_delete_stu"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataSetMeta",
            fields=[
                (
                    "dataset_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("subdata_id", models.CharField(blank=True, max_length=50, null=True)),
                ("dataset_design", models.TextField(blank=True, null=True)),
                ("dataset_citation", models.TextField(blank=True, null=True)),
                (
                    "data_platform",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("data_model", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "data_library",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("dataset_sample", models.TextField(blank=True, null=True)),
            ],
        ),
    ]