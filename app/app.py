import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
DB_PATH = 'data/tracker.db'

def init_db():
    """データベースとテーブルの初期化"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT DEFAULT (DATE('now', 'localtime')),
            mood INTEGER,
            condition TEXT,
            memo TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """メイン画面（履歴とグラフ表示）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # IDの新しい順（最新順）に取得
    cursor.execute('SELECT date, mood, condition, memo FROM records ORDER BY id DESC')
    records = cursor.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add_record():
    """記録の追加"""
    mood = request.form.get('mood')
    condition = request.form.get('condition')
    memo = request.form.get('memo')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO records (mood, condition, memo) VALUES (?, ?, ?)', (mood, condition, memo))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/api/data')
def get_data():
    """Chart.js用のデータをJSONで返すエンドポイント（最新の7件を古い順にソートして返す）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 🌟 バグ修正箇所: IDの降順で最新7件を確実に取得
    cursor.execute('SELECT date, mood FROM records ORDER BY id DESC LIMIT 7')
    rows = cursor.fetchall()
    conn.close()
    
    # グラフ描画用に時系列（古い順）に反転
    rows.reverse()
    
    labels = [row[0] for row in rows]
    moods = [row[1] for row in rows]
    
    return jsonify({'labels': labels, 'moods': moods})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)