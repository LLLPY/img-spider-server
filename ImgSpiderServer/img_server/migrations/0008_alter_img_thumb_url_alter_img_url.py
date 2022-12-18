# Generated by Django 4.1.3 on 2022-12-18 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("img_server", "0007_alter_img_thumb_url_alter_img_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="img",
            name="thumb_url",
            field=models.URLField(
                db_column="缩略图地址",
                help_text="缩略图地址",
                max_length=768,
                verbose_name="缩略图地址",
            ),
        ),
        migrations.AlterField(
            model_name="img",
            name="url",
            field=models.URLField(
                db_column="图片地址", help_text="图片地址", max_length=768, verbose_name="图片地址"
            ),
        ),
    ]
