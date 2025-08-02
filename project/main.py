import base64
import sqlite3
from flask import (
    Blueprint, render_template, request, jsonify, abort, redirect, url_for, current_app
)
from project.auth import login_required
from project.db import get_db, calculate_db_checksum, sync_state
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """主页，重定向到管理员页面。"""
    return redirect(url_for('main.admin'))

@bp.route('/admin')
@login_required
def admin():
    """管理后台页面，显示所有消息。"""
    db = get_db()
    messages = db.execute('SELECT * FROM messages ORDER BY id').fetchall()
    return render_template('main/admin.html', messages=messages)

@bp.route('/admin/add', methods=['POST'])
@login_required
def add_message():
    """添加新消息。"""
    message_id = request.form.get('id')
    content = request.form.get('content')

    if not message_id or not content:
        return jsonify({'success': False, 'error': '请提供ID和内容'}), 400

    db = get_db()
    try:
        db.execute('INSERT INTO messages (id, content) VALUES (?, ?)', (message_id, content))
        db.commit()
        sync_state['checksum'] = calculate_db_checksum()
        sync_state['last_modified'] = os.path.getmtime(current_app.config['DATABASE'])
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'ID已存在'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/admin/update', methods=['POST'])
@login_required
def update_message():
    """更新消息。"""
    message_id = request.form.get('id')
    content = request.form.get('content')

    if not message_id or not content:
        return jsonify({'success': False, 'error': '请提供ID和内容'}), 400

    db = get_db()
    try:
        cursor = db.execute('UPDATE messages SET content = ? WHERE id = ?', (content, message_id))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': '未找到该ID'}), 404
        
        sync_state['checksum'] = calculate_db_checksum()
        sync_state['last_modified'] = os.path.getmtime(current_app.config['DATABASE'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/admin/delete', methods=['POST'])
@login_required
def delete_message():
    """删除消息。"""
    message_id = request.form.get('id')
    if not message_id:
        return jsonify({'success': False, 'error': '请提供ID'}), 400

    db = get_db()
    try:
        cursor = db.execute('DELETE FROM messages WHERE id = ?', (message_id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': '未找到该ID'}), 404
        
        sync_state['checksum'] = calculate_db_checksum()
        sync_state['last_modified'] = os.path.getmtime(current_app.config['DATABASE'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<message_id>')
def get_message(message_id):
    """通过ID获取Base64编码的消息内容。"""
    db = get_db()
    message = db.execute('SELECT content FROM messages WHERE id = ?', (message_id,)).fetchone()
    if message:
        # 统一换行符为\n
        normalized_content = message['content'].replace('\r\n', '\n')
        encoded_content = base64.b64encode(normalized_content.encode()).decode()
        return encoded_content
    else:
        abort(404)
