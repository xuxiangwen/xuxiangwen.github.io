## 安装

### Docker

~~~shell
docker pull doccano/doccano
docker container create --name doccano \
  -e "ADMIN_USERNAME=admin" \
  -e "ADMIN_EMAIL=admin@example.com" \
  -e "ADMIN_PASSWORD=password" \
  -p 18000:8000 doccano/doccano
~~~

```
docker container start doccano
```

### [Dockers Compose](https://github.com/doccano/doccano#docker-compose)

~~~shell
git clone https://github.com/doccano/doccano.git
cd doccano
~~~

打开docker-compose.prod.yml文件修改superuser。

~~~shell
ADMIN_USERNAME: "admin"
ADMIN_PASSWORD: "password"
~~~

运行Doccano。

~~~shell
docker-compose -f docker-compose.dev.yml --env-file ./config/.env.example up
~~~

> 前端访问没有反应。

