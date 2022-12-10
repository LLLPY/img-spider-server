# Generated by Django 4.1.3 on 2022-12-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("img_server", "0003_img_api_img_err_msg_img_file_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="img",
            name="err_msg",
            field=models.CharField(
                db_column="错误信息",
                default="",
                help_text="错误信息",
                max_length=500,
                verbose_name="错误信息",
            ),
        ),
    ]
