import os
from flask import Flask, request, flash

def create_app(test_config=None):
    # 创建并配置应用
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),  # 默认密钥
        DATABASE=os.path.join(app.instance_path, 'data', 'messages.db'),
        ADMIN_FILE=os.path.join(app.instance_path, 'data', 'admin.json'),
    )

    if test_config is None:
        # 当不进行测试时，从文件加载实例配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 加载测试配置
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(os.path.join(app.instance_path, 'data'))
    except OSError:
        pass

    # 初始化数据库
    from . import db
    db.init_app(app)

    # 注册蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    # 在每个请求之前检查数据库变化
    @app.before_request
    def before_request():
        if not request.path.startswith('/static/'):
            if db.check_db_changes(app):
                flash('数据库内容已被外部程序修改，已同步最新数据', 'info')

    return app
