# Generated by Django 4.1.3 on 2022-12-17 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("page_server", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="api",
            name="url",
            field=models.URLField(
                db_column="接口地址",
                db_index=True,
                help_text="接口地址",
                max_length=1000,
                verbose_name="接口地址",
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="url",
            field=models.URLField(
                db_column="页面地址",
                db_index=True,
                help_text="页面地址",
                max_length=1000,
                verbose_name="页面地址",
            ),
        ),
    ]
