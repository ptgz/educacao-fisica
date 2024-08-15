import sqlite3, datetime
db = './main.db'

def _sendQuery(query, database = db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    res = cur.executescript(query)
    try:
        return res.fetchall()
    except:
        pass
    conn.close()
    

def _checkDbExists():
    try:
        conn = sqlite3.connect(db)
    except:
        return "Connection error: Could not connect to database " + db
    cur = conn.cursor()
    create_user_table = """
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  birthdate DATE,
  weight REAL,
  height REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_user_id ON user(id);
"""

    create_exercise_list_table = """
CREATE TABLE IF NOT EXISTS exercise_list (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES user(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_exercise_list_user_id ON exercise_list(user_id);
"""

    create_exercise_category_table = """
CREATE TABLE IF NOT EXISTS exercise_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT
);
CREATE INDEX idx_exercise_category_name ON exercise_category(name);
"""

    create_exercise_table = """
CREATE TABLE IF NOT EXISTS exercise (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  description TEXT,
  category_id INTEGER REFERENCES exercise_category(id),
  list_parent INTEGER REFERENCES exercise_list(id),
  series INTEGER,
  reps INTEGER,
  weight REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_exercise_name ON exercise(name);
CREATE INDEX idx_exercise_list_parent ON exercise(list_parent);
"""

    cur.executescript(create_user_table)
    cur.executescript(create_exercise_list_table)
    cur.executescript(create_exercise_category_table)
    cur.executescript(create_exercise_table)
    conn.close()
    return "OK"

def addUser(userInfo):
    ### fazer validação de informações de usuário aqui <
    name, birthdate, weight, height = userInfo
    _sendQuery(f"INSERT INTO user (name, birthdate, weight, height) VALUES ('{name}','{birthdate}', '{weight}', '{height}')")
    pass

def removeUser(userId):
    try:
        _sendQuery(f'DELETE FROM user WHERE id=={str(userId)}')
    except:
        return "ERROR"
    finally:
        return "OK"

def addExercise(exerciseInfo):
    pass

def removeExercise(exerciseInfo):
    pass

def attributeExercise(exerciseId, userId):
    pass

def createCategory(categoryInfo):
    pass

def removeCategory(categoryId):
    pass
