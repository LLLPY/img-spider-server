# Generated by Django 4.1.3 on 2022-11-24 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('page_server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(db_column='图片地址')),
                ('thumb_url', models.URLField(db_column='缩略图地址')),
                ('uid', models.CharField(db_column='唯一标识', max_length=100)),
                ('status', models.IntegerField(choices=[(0, '待爬取'), (1, '已爬取')], db_column='状态', default=0)),
                ('crawl_time', models.DateTimeField()),
                ('desc', models.CharField(db_column='图片描述', max_length=1000)),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page_server.keyword')),
                ('page_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page_server.page')),
            ],
        ),
    ]
