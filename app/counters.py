from .utils import connectDb
from fastapi import Depends
from datetime import datetime

# counters guarda as funções para controle de quantas informações foram inseridas
# no banco de dados em um dia

# adiciona 1 ao contador de assuntos do dia
def add1LessonCounter(database):
    conn = database[0]
    cursor = database[1]
    
    # verifica se já existe um contador pro dia de hoje
    cursor.execute('SELECT date FROM times_created_general\
                    WHERE date = NOW()::date')
    found_today = cursor.fetchall()
    
    if found_today:
        cursor.execute('UPDATE times_created_general\
                        SET lessons_created = lessons_created + 1\
                        WHERE date = NOW()::date')
    else:
        cursor.execute('INSERT INTO times_created_general(lessons_created)\
                         VALUES(1)')

    conn.commit()

# adiciona 1 ao contador de assuntos do dia
def add1SubjectCounter(database):
    conn = database[0]
    cursor = database[1]
    
    # verifica se já existe um contador pro dia de hoje
    cursor.execute('SELECT date FROM times_created_general\
                    WHERE date = NOW()::date')
    found_today = cursor.fetchall()
    
    if found_today:
        cursor.execute('UPDATE times_created_general\
                        SET subjects_created = subjects_created + 1\
                        WHERE date = NOW()::date')
    else:
        cursor.execute('INSERT INTO times_created_general(subjects_created)\
                         VALUES(1)')

    conn.commit()

# adiciona 1 ao contador de usuáriso criados do dia
def add1UsersCreatedCounter(database):
    conn = database[0]
    cursor = database[1]
    
    # verifica se já existe um contador pro dia de hoje
    cursor.execute('SELECT date FROM times_created_general\
                    WHERE date = NOW()::date')
    found_today = cursor.fetchall()
    
    if found_today:
        cursor.execute('UPDATE times_created_general\
                        SET users_created = users_created + 1\
                        WHERE date = NOW()::date')
    else:
        cursor.execute('INSERT INTO times_created_general(users_created)\
                         VALUES(1)')

    conn.commit()