## 项目介绍
  根据从grafana里得到的存有VM名称的csv文件，从gic数据库中查到客户信息，并更新或新增到新的表格里。
### 项目简介
flask开发的节点web程序，前端引用了部分bootstrap框架。  
post请求返回信息格式如下：
```
$ curl -H 'Content-Type: application/json' -XPOST 'http://10.13.2.133:6101/v1/resop/vm/vm_info/'  -d '{"vm_name": "E048439-centos6.864-20170629104416-FPUP953C"}'

{"code_msg":"success","message":"operation success","code":"0000","data":{"customer_contacts":"None","customer_email":"fckman.com@gmail.com","public_ip":"118.193.23.247","customer_mobile":"fckman.com@gmail.com","private_ip":"10.240.0.2","customer_name":"fckman.com@gmail.com"}}
```
用到的服务：
1. nginx：高性能Web服务器+负责反向代理；
2. gunicorn：高性能WSGI服务器；
3. gevent：把Python同步代码变成异步协程的库；
4. supervisor：监控服务进程的工具；

### 镜像制作
1. docker image的制作详见Dockerfile
2. 制作镜像： docker build -t get_vm_info:v1 .
### 部署
目前已经把制作好的镜像上传到私有docker仓库，只需要下载下来启动即可：  
启动镜像： docker run -p 8001:80 -d --name get_vm_info direpos.capitalonline.net/get_vm_info:v1  