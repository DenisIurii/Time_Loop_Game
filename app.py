from flask import Flask, render_template, redirect, url_for, request, session, g, jsonify
import sqlite3, os, json, datetime, random
from story import story, SECRET_ADMIN_KEY, ENDINGS_LIST

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change_me")

DB = 'progress.db'
MAX_HISTORY = 20

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

ef init_db():
    db = get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS saves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        scene_id TEXT NOT NULL,
        data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS fragments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        text,
        found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    db.commit()

with app.app_context():
    init_db()

@app.route('/')
def index():
    session.setdefault('fatigue', 0)
    session.setdefault('theme', 'normal')
    return render_template('index.html')

@app.route('/scene/<scene_id>')
def scene(scene_id):
    data = story.get(scene_id)
    if not data:
        return redirect(url_for('index'))
    session['current_scene'] = scene_id
    history = session.get('history', [])
    history.append(scene_id)
    session['history'] = history[-MAX_HISTORY:]
    return render_template('scene.html', scene=data, scene_id=scene_id, history=session['history'], anomaly=False, anomaly_level=0, fatigue=session.get('fatigue',0), player_name=session.get('player_name'), palette=session.get('theme','normal'))

@app.route('/choice', methods=['POST'])
def choice():
    next_scene = request.form.get('next')
    if request.form.get('autosave') == '1':
        db = get_db()
        db.execute('INSERT INTO saves (name, scene_id, data) VALUES (?,?,?)', ('AutoSave', next_scene, json.dumps({'scene':next_scene})))
        db.commit()
    return redirect(url_for('scene', scene_id=next_scene))

@app.route('/api/save', methods=['POST'])
def api_save():
    name = request.form.get('name','Save')
    scene = session.get('current_scene','start')
    db = get_db()
    cur = db.execute('INSERT INTO saves (name, scene_id, data) VALUES (?,?,?)', (name, scene, json.dumps({'scene':scene})))
    db.commit()
    return jsonify({'status':'ok','save_id': cur.lastrowid})

@app.route('/saves')
def saves():
    db = get_db()
    rows = db.execute('SELECT id,name,scene_id,created_at FROM saves ORDER BY created_at DESC').fetchall()
    return render_template('saves.html', saves=rows)

@app.route('/memory')
def memory():
    db = get_db()
    rows = db.execute('SELECT key,text,found_at FROM fragments ORDER BY id').fetchall()
    return render_template('memory.html', fragments=rows)

if __name__ == '__main__':
    app.run(debug=True)

