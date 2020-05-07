## 特殊开发及运行环境要求
- Python>3.5 推荐使用 3.6.4
- celery<3.1.22

## 测试服务器相关信息
- HOST
    - host: 192.168.3.87
    - username: dmp
    - password: dmp123.
    
- MySQL
    - host: 192.168.3.87
    - port: 3306
    - username: root
    - password: shtd123.
    
- Redis
    - host: 192.168.3.87
    - port: 6379
    
- RabbitMQ
    - host: 191.168.3.87
    - server_port: 5672
    - web_management_port: 15672
    - username: dmp
    - password: dmp123.

## run 
```shell script
# install requirement
pip install -r requirements.txt
# celery worker
nohup ./celery_run.sh &
# flask server
python manage.py runserver
```
