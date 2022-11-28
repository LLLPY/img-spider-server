# Generated by Django 4.1.3 on 2022-11-28 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("img_server", "0005_rename_page_url_img_page_alter_img_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="img",
            name="qualify",
            field=models.IntegerField(
                choices=[(0, "合格"), (1, "不合格")],
                db_column="是否合格",
                default=0,
                verbose_name="是否合格",
            ),
        ),
    ]
