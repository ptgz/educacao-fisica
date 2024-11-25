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

## PRA HOJE:::::::::

def addExercise(exerciseInfo):
    name, description, category_id, list_parent, series, reps, weight = exerciseInfo          # name, description, category_id, list_parent, series, reps, weight
    _sendQuery(f"INSERT INTO exercise (name, description, category_id, list_parent, series, reps, weight) VALUES ('{name}','{description}', '{category_id}', '{list_parent}', '{series}', '{reps}', '{weight}')")
    pass

def removeExercise(exerciseId):
    try:
        _sendQuery(f'DELETE FROM exercise WHERE id=={str(exerciseId)}')
        return "OK"
    except:
        return "ERROR"
    pass


def getExercises():
    try:
        res = _sendQuery('SELECT id FROM exercise')
        return res
    except:
        return "ERROR"

def getExerciseById(exerciseId):
    try:
        res = _sendQuery(f'SELECT * FROM exercise WHERE id =={str(exerciseId)}')
        return res
    except:
        return "ERROR"

def updateExercise(exerciseId, toChange):  # tochange deve ser uma lista de dicionarios com valores a alterar, por exemplo, para alterar "name" para "joão", seria >>> [{"name" : "joão"}]
    toQuery = []
    for change in toChange:
        toQuery.append(f'UPDATE exercise SET {change} = {toChange[change]} WHERE id == {exerciseId}')
    
    mainQuery = ";".join(toQuery)
    try:
        _sendQuery(mainQuery)
        return "OK"
    except:
        return "ERROR"

## PRA HOJE /\/\/\/\/\//\/\/\/\/\

def attributeExercise(exerciseId, userId):
    # Verificar se os usuários existem
    try:
        exercise_exists = _sendQuery(f"SELECT id FROM exercise WHERE id = {exerciseId}")
        user_exists = _sendQuery(f"SELECT id FROM user WHERE id = {userId}")
        
        if not exercise_exists:
            return f"ERRO: Exercicio com ID {exerciseId} não existe."
        
        if not user_exists:
            return f"ERRO: Usuario com ID {userId} não existe."
        
        # Atribuir o exercício ao usuário
        _sendQuery(f"INSERT INTO user_exercise (user_id, exercise_id) VALUES ({userId}, {exerciseId})")
        return "OK"
    except Exception as e:
        return f"ERROR: {str(e)}"


def createCategory(categoryInfo):
    # categoryInfo deve ser uma tupla ou lista contendo o nome da categoria
    category_name = categoryInfo[0]

    # Verificar se a categoria já existe
    existing_category = _sendQuery(f"SELECT id FROM exercise_category WHERE name = '{category_name}'")
    
    if existing_category:
        return f"ERROR: Categoria '{category_name}' já existe."
    
    # Inserir nova categoria
    try:
        _sendQuery(f"INSERT INTO exercise_category (name) VALUES ('{category_name}')")
        return "OK"
    except Exception as e:
        return f"ERRO: {str(e)}"


def removeCategory(categoryId):
    # Verificar se a categoria existe
    existing_category = _sendQuery(f"SELECT id FROM exercise_category WHERE id = {categoryId}")
    
    if not existing_category:
        return f"ERROR: Categoria com ID {categoryId} não existe."

    # Verificar se há exercícios usando essa categoria
    associated_exercises = _sendQuery(f"SELECT id FROM exercise WHERE category_id = {categoryId}")
    
    if associated_exercises:
        return "ERROR: Não é possível remover esta categoria; pois tem exercicios associados a ela."
    
    # Remover a categoria
    try:
        _sendQuery(f"DELETE FROM exercise_category WHERE id = {categoryId}")
        return "OK"
    except Exception as e:
        return f"ERROR: {str(e)}"
