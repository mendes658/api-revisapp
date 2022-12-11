from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends, Request
from .. import utils, schemas, oauth2
import datetime

router = APIRouter()
subjects = {}

@router.post('/add_lesson', status_code=status.HTTP_201_CREATED)
def addLesson(request: Request, post: schemas.AddLesson, database = Depends(utils.connectDb)):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    user = oauth2.getCurrentUser(token)
    
    conn = database[0]
    cursor = database[1]
    
    print(post.first_rev_date)
    print(post.last_rev_date)
    print(post.date)

    cursor.execute('SELECT id FROM subjects WHERE user_id = %s and subject_name = %s',(user, post.chosen_subject))
    subjectID = cursor.fetchone()

    if not subjectID:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No subject found')
    else:
        cursor.execute('INSERT INTO lessons (lesson, subject_id, revision_dates, first_rev_date, last_rev_date, date)\
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;', 
        (post.lesson, subjectID['id'], post.revision_dates, post.first_rev_date, post.last_rev_date, post.date))
        
        created = cursor.fetchall()
        conn.commit()

        return created



@router.get('/get_lessons/{subject}')
def getLessons(request: Request, subject: str, database = Depends(utils.connectDb)):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    user = oauth2.getCurrentUser(token)
    
    cursor = database[1]
    try:
        cursor.execute('SELECT lessons.id, lessons.lesson, lessons.created_at\
                        FROM lessons\
                        INNER JOIN subjects ON subjects.id = lessons.subject_id\
                        INNER JOIN users ON users.id = subjects.user_id\
                        WHERE users.id = %s AND subjects.subject_name = %s;',(user, subject))
    except Exception as error:
        return error
    
    got = cursor.fetchall()

    listGot = [[i['id'], i['lesson'], i['created_at'].strftime('%d/%m/%Y')] for i in got]

    return {"lessons": listGot}



# update front-end to switch from list to string separated by commas
@router.post('/delete_lessons', status_code=status.HTTP_200_OK)
def deleteLessons(request: Request, post: schemas.DeleteLesson, database = Depends(utils.connectDb)):

    ids = post.ids
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    user = oauth2.getCurrentUser(token)

    conn = database[0]
    cursor = database[1]

    for id_ in ids:
        cursor.execute('DELETE FROM lessons\
                        USING subjects, users\
                        WHERE lessons.id = %s AND users.id = %s\
                        AND users.id = subjects.user_id\
                        AND subjects.id = lessons.subject_id RETURNING *;', (id_, user))
    try:
        last_deleted = cursor.fetchall()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No lesson found')
    
    conn.commit()
    


