#nginx的配置文件
cp img_spider_server.conf /etc/nginx/conf.d/

#关闭占用的8001端口
kill -9 $(lsof -i:8001)

#启动uwsgi
uwsgi uwsgi.ini

#从新加载nginx
service nginx reload

echo "启动成功!"
