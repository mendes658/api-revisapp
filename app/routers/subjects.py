from fastapi import Response, status, HTTPException, APIRouter, Depends, Request
from .. import utils, schemas, oauth2, counters
from datetime import datetime, timezone, timedelta
import psycopg2

router = APIRouter()
subjects = {}

def getlast11days():
    last11 = []
    
    now = datetime.now(timezone.utc).astimezone()
    for i in range(11):
        nowStr = now.strftime('%Y-%m-%d')
        last11.append(nowStr)
        now = now - timedelta(days=1)
    return last11


@router.post('/add_subject', status_code=status.HTTP_201_CREATED)
def addSubject(request: Request, subject: schemas.AddSubject, database = Depends(utils.connectDb)):
    
    token = request.cookies['acess_token'].split()[1]
    user = oauth2.getCurrentUser(token)

    conn = database[0]
    cursor = database[1]

    cursor.execute('SELECT * FROM subjects WHERE user_id = %s AND subject_name = %s', (user, subject.subject))
    
    subjectAlreadyOnDB = cursor.fetchall()
    if subjectAlreadyOnDB:
        raise HTTPException(status.HTTP_409_CONFLICT, detail= f'Subject already exists')
    elif len(subject.subject) > 25:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE  , detail= f'Subject length > 25')
    else:
        counters.add1SubjectCounter(database)

        cursor.execute('INSERT INTO subjects (subject_name, user_id) VALUES (%s, %s) RETURNING *', (
            subject.subject, user
        ))
        created = cursor.fetchone()
        conn.commit()
        created.added = True

 
        return created


@router.get('/get_all_subjects')
def getSubjects(request: Request, database = Depends(utils.connectDb)):
    
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    
    user = oauth2.getCurrentUser(token)
    cursor = database[1]
    
    cursor.execute('SELECT subjects.subject_name, COUNT(lessons.subject_id) AS total_lessons\
                    FROM subjects\
                    FULL JOIN lessons ON subjects.id = lessons.subject_id\
                    WHERE subjects.user_id = %s\
                    GROUP BY subjects.subject_name;', (user,))
    
    subjectAndTotalLessons = cursor.fetchall()
    subsList = []

    for dic in subjectAndTotalLessons:
        subsList.append([dic['subject_name'], dic['total_lessons']])

    return {"subjects": subsList}

@router.post('/delete_subjects/', status_code=status.HTTP_200_OK)
def deleteSubjects(request: Request, subjects: schemas.DeleteSubjects, database = Depends(utils.connectDb)):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    
    user = oauth2.getCurrentUser(token)

    conn = database[0]
    cursor = database[1]

    for subject in subjects.subjects:
        cursor.execute('DELETE FROM subjects WHERE subject_name = %s \
                        AND user_id = %s RETURNING *;', (subject, user))
    try:
        deleted = cursor.fetchone()
        conn.commit()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No subject found')

@router.get('/get_all_revisions')
def getAllRevisions(request: Request, database = Depends(utils.connectDb)):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    
    user = oauth2.getCurrentUser(token)

    cursor = database[1]
    cursor.execute("SELECT subjects.subject_name, string_agg(lessons.revision_dates, ',') AS all_revisions FROM subjects\
                    INNER JOIN lessons ON subjects.id = lessons.subject_id\
                    INNER JOIN users ON users.id = subjects.user_id\
                    WHERE users.id = %s\
                    GROUP BY subjects.subject_name;",(user,))
    
    allRevisions = {}
    try:
        revisionsDict = cursor.fetchall()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No subject found')

    for i in revisionsDict:
        if i['all_revisions'] != None:
            revs = i['all_revisions'].split(',')
            subject = i['subject_name']
            for rev in revs:
                year = rev[0:4]
                month = rev[5:7]
                day = rev[8:10]
                formated = f'{year}-{month}-{day}'
                if allRevisions.get(formated) and subject not in allRevisions[formated]:
                    allRevisions[formated].append(subject)
                else:
                    allRevisions[formated] = [subject]
    
    return {"allRevisions": allRevisions}

@router.get('/get_last11_studied')
def getLast11(request: Request, database = Depends(utils.connectDb)):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    
    user = oauth2.getCurrentUser(token)
    cursor = database[1]

    tomorrow = datetime.now(timezone.utc).astimezone() + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    before_12 = datetime.now(timezone.utc).astimezone() - timedelta(days=11)
    before_12 = before_12.strftime('%Y-%m-%d')
    try:
        cursor.execute("SELECT subjects.subject_name, array_agg(lessons.date) AS all_dates FROM lessons\
                        FULL JOIN subjects ON subjects.id = lessons.subject_id\
                        FULL JOIN users ON users.id = subjects.user_id\
                        WHERE users.id = %s AND\
                        %s < lessons.date AND\
                        lessons.date < %s\
                        GROUP BY subjects.subject_name",(user, str(before_12), str(tomorrow)))
    except psycopg2.errors.NullValueNotAllowed:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No subject found')
    
    try:
        subsDict = cursor.fetchall()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No subject found')

    subsWithLessonAmount = {}

    for i in subsDict:
        revs = i['all_dates']
        subject = i['subject_name']
        last11 = {k:0 for k in getlast11days()}
        for rev in revs:
            dateStr = rev.strftime('%Y-%m-%d')
            last11[dateStr] = last11.get(dateStr, 0) + 1
        subsWithLessonAmount[subject] = list(last11.values())[::-1]

    return {"last11": subsWithLessonAmount}
    
@router.get('/get_todays_revisions/{date}')
def getTodaysRevision(date: str, request: Request, database = Depends(utils.connectDb)):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    user = oauth2.getCurrentUser(token)
    cursor = database[1]
    
    chosenYear = int(date[0:4])
    chosenMonth = int(date[5:7])
    chosenDay = int(date[8:])
    chosenDate = datetime(chosenYear, chosenMonth, chosenDay)

    tomorrow = chosenDate.astimezone() + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    yesterday = chosenDate.astimezone() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    
    try:
        cursor.execute("SELECT lessons.lesson, subjects.subject_name, string_agg(lessons.revision_dates , ',') AS all_revisions FROM lessons\
                        INNER JOIN subjects ON subjects.id = lessons.subject_id\
                        FULL JOIN users ON users.id = subjects.user_id\
                        WHERE users.id = %s AND\
                        lessons.first_rev_date < %s AND\
                        lessons.last_rev_date > %s\
                        GROUP BY lessons.id, subjects.subject_name",(user, tomorrow, yesterday))
    except:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No lessons found')

    try:
        allLessons = cursor.fetchall() #[('lesson', 'organic_chemistry'), ('subject_name', 'chemistry'), ('all_revisions', '2022-11-16T00:00:00.000Z,2022-11...')]
        print(allLessons)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No lessons found')

    todaysLessons = [] #['subject', 'lesson']
    for i in allLessons:
        formatedRevisions = [rev[0:10] for rev in i['all_revisions'].split(',')]
        if date in formatedRevisions:
            todaysLessons.append([i['subject_name'], i['lesson']])

    return {"todaysRevisions": todaysLessons}