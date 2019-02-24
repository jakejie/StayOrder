# 项目开发/部署说明

## 环境部署
    1.安装python3
        Ubuntu16 自带python3环境
    2.安装pip依赖工具
        Ubuntu：sudo apt-get install python3-pip
    3.建立虚拟环境(推荐使用虚拟环境进行配置)
        1.安装virtalenv :pip3 install virtualenv
        2.在home目录下创建虚拟环境：
            cd /home 回车
            virtualenv --python=python3 crawl_env
            指定使用python3 虚拟环境名crawl_env
    4.安装其他依赖
        1.MySQL数据库安装
            sudo apt-get install mysql-server
            sudo apt install mysql-client
            sudo apt install libmysqlclient-dev
            使用默认配置就行 不需要修改host
        2.创建数据库
            数据库名:stayorder
            备注：数据库字符集：utf8mb4 -- UTF-8 Unicode
                  排序方式：utf8mb4_general_ci
            防止因为编码问题导致数据入库失败
        3.安装uwsgi
            pip install uwsgi
    
    5.安装依赖库
        1.激活虚拟环境(若没有使用虚拟环境 则跳过该步骤)
            source /home/crawl_env/bin/activate
        2.安装依赖包--指定文件：代码里的requirements.txt文件
            pip3 install -r requirements.txt 回车
    6.环境配置完毕
        系统python3环境配置完成
    
    7.安装rz工具 服务器快速上传文件
        sudo apt-get install lrzsz


## 操作步骤 如下
    

#### 1 启动web后端
    1.nginx配置(略)
    2.uwsgi配置(参考文件)
    3.修改StayOrder/uwsgi_Tscript/uwsgi.ini文件中的 项目路径/解释器路径/运行端口/进程数
        根据文件注释 进行相应修改即可 注意端口和nginx中的配置 是否一致
    3.启动 uwsgi uwsgi.ini

#### 2 启动爬虫
    python3 crawler.py
    或者 后台运行：
    nohup python3 crawler.py &
    

## 其他说明

### web界面
#### 1.登录页面
    地址：login/

#### 2.预约数据提交页
    地址：index/

#### 3.查看历史提交记录页
    地址：history/

#### 参数配置 StayOrder/StayOrder/settings.py文件
    !!!!!!此处数据库配置务必和爬虫端配置保持一致
    DEBUG = True               # 开启调试模式
    ALLOWED_HOSTS = ["*"]      # 部署的域名 *表示任意
    # 数据库参数配置 DATABASES(代码80行左右)
    1.'NAME': 'stayorder',     # 数据库名称
    2.'HOST': '',              # 数据库IP
    3.'USER': 'root',          # 数据库用户名
    4.'PASSWORD': ''           # 数据库连接密码

### 爬虫端

#### 参数配置 StayOrder/apps/order/config.py
    !!!!!!此处数据库配置务必和web端配置保持一致
    # 数据库相关参数配置
    db_user = 'root'        # 数据库用户名
    db_pawd = ''            # 数据库连接密码
    db_host = ''            # 数据库IP
    db_port = 3306          # 数据库端口
    db_name = 'stayorder'   # 数据库名称
    
    # 邮件服务器配置
    EMAIL_HOST = "smtp.163.com"     # 邮件服务器主机
    EMAIL_HOST_USER = ""            # 邮件发送帐号
    EMAIL_HOST_PASSWORD = ""        # 邮件发送密码
    
    # 代理IP配置
    USE_PROXY = False               # 是否使用代理
    proxy_url = ""                  # 讯代理 代理ip提取地址

    # REDIS配置 / 代理ip池
    REDIS_HOST = "127.0.0.1"        # REDIS主机
    REDIS_PORT = "6379"             # REDIS端口
    REDIS_DB_PROXY = 12             # REDIS库
    REDIS_DB_KEY = "proxy"          # REDIS 的 KEY
    
    # 爬虫间隔时间/单位：秒
    CRAWL_PERIOD = 15
    
    # 超级鹰 配置
    username = ""  # 超级鹰用户名
    password = ""  # 超级鹰密码
    soft_id = ""  # 超级鹰 应用ID
