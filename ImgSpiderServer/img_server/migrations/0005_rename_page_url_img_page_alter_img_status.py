# Generated by Django 4.1.3 on 2022-11-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("img_server", "0004_img_source"),
    ]

    operations = [
        migrations.RenameField(
            model_name="img",
            old_name="page_url",
            new_name="page",
        ),
        migrations.AlterField(
            model_name="img",
            name="status",
            field=models.IntegerField(
                choices=[(0, "待爬取"), (1, "爬取中"), (2, "已爬取"), (3, "爬取错误")],
                db_column="状态",
                default=0,
                verbose_name="状态",
            ),
        ),
    ]
