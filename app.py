import base64
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

app = Flask(__name__)

# 数据库配置
DATABASE = 'data.db'

# 确保数据库目录存在
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        content TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# 获取数据库连接
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
init_db()

# 主页路由 - 重定向到管理页面
@app.route('/')
def index():
    return redirect(url_for('admin'))

# 管理页面路由
@app.route('/admin')
def admin():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
    conn.close()
    return render_template('admin.html', messages=messages)

# 添加消息路由
@app.route('/admin/add', methods=['POST'])
def add_message():
    message_id = request.form.get('id')
    content = request.form.get('content')

    if not message_id or not content:
        return jsonify({'success': False, 'error': '请提供ID和内容'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO messages (id, content) VALUES (?, ?)',
                      (message_id, content))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'error': 'ID已存在'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500

# 更新消息路由
@app.route('/admin/update', methods=['POST'])
def update_message():
    message_id = request.form.get('id')
    content = request.form.get('content')

    if not message_id or not content:
        return jsonify({'success': False, 'error': '请提供ID和内容'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('UPDATE messages SET content = ? WHERE id = ?',
                      (content, message_id))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': '未找到该ID'}), 404

        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500

# 删除消息路由
@app.route('/admin/delete', methods=['POST'])
def delete_message():
    message_id = request.form.get('id')

    if not message_id:
        return jsonify({'success': False, 'error': '请提供ID'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': '未找到该ID'}), 404

        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500

# 通过ID获取base64编码的内容
@app.route('/<message_id>')
def get_message(message_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM messages WHERE id = ?', (message_id,))
    message = cursor.fetchone()
    conn.close()

    if message:
        # 将文本内容转换为base64编码
        encoded_content = base64.b64encode(message['content'].encode()).decode()
        return encoded_content
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
