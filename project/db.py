import os
import sqlite3
import hashlib
from datetime import datetime
from flask import current_app, g, flash

# 使用一个字典来存储同步状态，避免使用全局变量
sync_state = {
    'last_modified': 0,
    'checksum': ""
}

def get_db():
    """获取当前请求的数据库连接。"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """关闭数据库连接。"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """初始化数据库表结构。"""
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL
        )
    ''')
    db.commit()

def calculate_db_checksum():
    """计算数据库内容的校验和。"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, content FROM messages ORDER BY id')
    rows = cursor.fetchall()
    content_str = "".join([f"{row['id']}:{row['content']};" for row in rows])
    return hashlib.md5(content_str.encode()).hexdigest()

def check_db_changes(app):
    """检查数据库文件是否有变化。"""
    db_path = app.config['DATABASE']
    if not os.path.exists(db_path):
        return False

    current_mtime = os.path.getmtime(db_path)

    if current_mtime > sync_state['last_modified'] or not sync_state['checksum']:
        new_checksum = calculate_db_checksum()
        if new_checksum != sync_state['checksum']:
            sync_state['checksum'] = new_checksum
            sync_state['last_modified'] = current_mtime
            app.logger.info(f"数据库内容已变化，同步于 {datetime.now()}")
            return True
        sync_state['last_modified'] = current_mtime
    return False

def init_app(app):
    """注册数据库命令和应用关闭时的清理操作。"""
    app.teardown_appcontext(close_db)

    # 在应用上下文中初始化数据库和校验和
    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            init_db()
        sync_state['checksum'] = calculate_db_checksum()
        if os.path.exists(app.config['DATABASE']):
            sync_state['last_modified'] = os.path.getmtime(app.config['DATABASE'])
