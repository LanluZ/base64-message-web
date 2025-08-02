# 消息管理系统

这是一个基于 Flask 的简单消息管理系统，允许管理员登录并对消息进行增、删、改、查操作。

## 预览

![](/images/001.png)
![](/images/002.png)

## 特性

-   **用户认证**: 安全的管理员登录和登出功能。
-   **消息管理**: 对消息进行 CRUD (创建, 读取, 更新, 删除) 操作。
-   **动态同步**: 实时检测数据库文件的外部修改并自动同步。
-   **RESTful API**: 提供一个通过 ID 获取 Base64 编码消息内容的接口。

## 技术栈

-   **后端**: Flask
-   **数据库**: SQLite
-   **前端**: Bootstrap 5, jQuery

## 部署指南

### 前提条件

- Python 3.6+
- pip (Python包管理器)

### 部署

**明文在公网上传输是十分不安全的做法, 部署前请务必准备好SSL证书**

1. 部署前需创建`instance`目录并写入管理员信息

2. Linux
   ```bash
   pip install gunicorn
   pip install gevent
   gunicorn -w 4 -k gevent -b 0.0.0.0:[端口] --preload run:app
   ```
3. Windows
   ```bash
   python run.py 
   ```

### 关于`instance`目录

`instance`目录包含特定于实例的配置和数据，不应该被推送到版本控制系统（如Git）中。这个目录包含：

- `data/admin.json`: 管理员用户凭据
- `data/messages.db`: SQLite数据库，存储应用程序的消息数据
- `config.py` (可选): 覆盖默认配置的自定义配置文件

```json
{
    "admins": [
        {
            "username": "1",
            "password": "1",
            "display_name": "1",
            "role": "super_admin",
            "email": "admin@example.com"
        },
        {
            "username": "2",
            "password": "2",
            "display_name": "2",
            "role": "editor",
            "email": "editor@example.com"
        }
    ]
}

```
