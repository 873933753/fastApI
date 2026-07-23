# web目录放路由
# models目录放模型设计，用来建表
# libs - 辅助函数
# setting文件 - 常用变量

# 1、确认本地数据库已经连接

# 2、确认redis已连接
## 1）启动docker中的redis-dev容器
## 2）连接redis - docker exec -it redis-dev redis-cli

# 3、启动项目
## 1）cd fisher
## 2）激活虚拟环境 
## 3）启动命令  .\venv\Scripts\python.exe index.py


# 安装包需要写入requirements.txt
```
pip freeze | findstr python-multipart
```

# 启动无法加载检查端口是否被占用
```
端口问题-停端口
netstat -ano | findstr ":8000"
Stop-Process -Id 2884 -Force
```