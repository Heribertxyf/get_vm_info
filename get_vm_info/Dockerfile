# FROM direpos.capitalonline.net/cdsops-alpine:base
FROM alpine:latest

MAINTAINER xujpxm

ENV ENV_CONFIG production
#创建代码目录
RUN mkdir -p /data/get_vm_info \
    && apk update \
    && apk add --no-cache nginx py-pip tzdata py-gevent supervisor py-mysqldb\
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone \ 
    && apk del tzdata \
    && mkdir /run/nginx/ \
    && mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak 

#上传代码和nginx+supervisor服务的配置文件
ADD . /data/get_vm_info
ADD conf/nginx_example.conf /etc/nginx/conf.d/
ADD conf/supervisor_example.ini /etc/supervisor.d/

EXPOSE 80

#安装代码运行依赖包
WORKDIR /data/get_vm_info/
# 额外安装tzdata，配置tiemzone为中国
RUN  pip install --no-cache-dir -r requirements.txt

# 启动supervisor，配置文件里包含nginx和gunicorn,相当于同时启动两个服务
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]