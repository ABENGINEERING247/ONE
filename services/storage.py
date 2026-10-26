import sqlite3
from datetime import datetime
from services.config import DB_PATH

def _connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with _connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            idea TEXT NOT NULL,
            paper TEXT NOT NULL,
            sources TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'Draft',
            updated_at TEXT NOT NULL
        )""")
        con.commit()

def create_project(project):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with _connect() as con:
        cur = con.execute("INSERT INTO projects(title,idea,paper,sources,status,updated_at) VALUES(?,?,?,?,?,?)",
                          (project["title"], project["idea"], project["paper"], _dump(project.get("sources", [])), project.get("status","Draft"), now))
        con.commit()
        return cur.lastrowid

def save_project(project):
    import json
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with _connect() as con:
        con.execute("""INSERT INTO projects(id,title,idea,paper,sources,status,updated_at)
        VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title, idea=excluded.idea,
        paper=excluded.paper, sources=excluded.sources, status=excluded.status, updated_at=excluded.updated_at""",
        (project.get("id"), project["title"], project["idea"], project["paper"], json.dumps(project.get("sources", [])),
         project.get("status","Draft"), now))
        con.commit()
    return project.get("id")

def list_projects():
    with _connect() as con:
        rows = con.execute("SELECT id,title,updated_at FROM projects ORDER BY updated_at DESC").fetchall()
    return [{"id": r[0], "title": r[1], "updated_at": r[2]} for r in rows]

def load_project(project_id):
    import json
    with _connect() as con:
        row = con.execute("SELECT id,title,idea,paper,sources,status,updated_at FROM projects WHERE id=?", (project_id,)).fetchone()
    if not row:
        return None
    return {"id":row[0],"title":row[1],"idea":row[2],"paper":row[3],"sources":json.loads(row[4] or "[]"),"status":row[5],"updated_at":row[6]}

def _dump(value):
    import json
    return json.dumps(value, ensure_ascii=False)
