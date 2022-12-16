from fastapi import HTTPException, status

# counters guarda as funções para controle de quantas informações foram inseridas
# no banco de dados em um dia

# limite de criações por dia
LESSON_LIMIT = 10000
USERS_LIMIT = 1500
SUBJECTS_LIMIT = 5000

# adiciona 1 ao contador de assuntos do dia
def add1LessonCounter(database):
    conn = database[0]
    cursor = database[1]
    
    # verifica se já existe um contador pro dia de hoje
    cursor.execute('SELECT lessons_created FROM times_created_general\
                    WHERE date = NOW()::date')
    found_today = cursor.fetchone()
    
    if found_today:
        found_today = int(found_today['lessons_created'])
        if found_today >= LESSON_LIMIT:
             raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail='Day limit exceeded')

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
    cursor.execute('SELECT subjects_created FROM times_created_general\
                    WHERE date = NOW()::date')
    found_today = cursor.fetchone()

    if found_today:
        found_today = int(found_today['subjects_created'])
        if found_today >= SUBJECTS_LIMIT:
             raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail='Day limit exceeded')
        
        cursor.execute('UPDATE times_created_general\
                        SET subjects_created = subjects_created + 1\
                        WHERE date = NOW()::date')
    else:
        cursor.execute('INSERT INTO times_created_general(subjects_created)\
                         VALUES(1)')

    conn.commit()

# adiciona 1 ao contador de usuários criados do dia
def add1UsersCreatedCounter(database):
    conn = database[0]
    cursor = database[1]
    
    # verifica se já existe um contador pro dia de hoje
    cursor.execute('SELECT users_created FROM times_created_general\
                    WHERE date = NOW()::date')
    found_today = cursor.fetchone()

    if found_today:
        found_today = int(found_today['users_created'])
        if found_today >= USERS_LIMIT:
             raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail='Day limit exceeded')
        
        cursor.execute('UPDATE times_created_general\
                        SET users_created = users_created + 1\
                        WHERE date = NOW()::date')
    else:
        cursor.execute('INSERT INTO times_created_general(users_created)\
                         VALUES(1)')

    conn.commit()