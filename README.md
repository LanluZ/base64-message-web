# 消息管理系统

这是一个基于 Flask 的简单消息管理系统，允许管理员登录并对消息进行增、删、改、查操作。

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

### 安装步骤

1. 克隆仓库
   ```bash
   git clone <repository-url>
   cd FlaskProject1
   ```

2. 创建并激活虚拟环境
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖项
   ```bash
   pip install -r requirements.txt
   ```

4. 设置`instance`目录
   - 创建必要的目录结构
     ```bash
     mkdir -p instance/data
     ```
   - 创建管理员配置文件`instance/data/admin.json`
     ```json
     {
       "username": "admin",
       "password": "your-secure-password",
       "role": "admin"
     }
     ```
   - 初始化数据库
     ```bash
     flask --app project init-db
     ```

5. 运行应用程序
   ```bash
   python run.py
   ```
   应用程序将在`http://localhost:5000`上运行

### 关于`instance`目录

`instance`目录包含特定于实例的配置和数据，不应该被推送到版本控制系统（如Git）中。这个目录包含：

- `data/admin.json`: 管理员用户凭据
- `data/messages.db`: SQLite数据库，存储应用程序的消息数据
- `config.py` (可选): 覆盖默认配置的自定义配置文件

### 自定义配置

你可以创建一个`instance/config.py`文件来覆盖默认配置：

```python
# 示例配置
SECRET_KEY = 'your-secret-key'  # 覆盖随机生成的密钥
# 其他自定义配置...
```

## 使用指南

1. 访问`http://localhost:5000`查看主页
2. 访问`http://localhost:5000/login`登录管理员账户
3. 登录后，你可以访问管理员面板管理消息
