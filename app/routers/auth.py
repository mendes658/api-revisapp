from fastapi import Response, status, HTTPException, APIRouter, Depends, Request
from .. import utils, schemas, oauth2, counters
import psycopg2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter()

@router.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserOut)
def createUser(user: schemas.CreateUser, database = Depends(utils.connectDb)):
    
    conn = database[0]
    cursor = database[1]
    
    password = utils.hash(user.password)

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *;', (
            user.username, password
        ))
        created = cursor.fetchone()
        conn.commit()

        counters.add1UsersCreatedCounter(database)
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status.HTTP_409_CONFLICT, detail= f'User already exists')
    
    return created

@router.post('/login')
def login(response: Response, userInfo: OAuth2PasswordRequestForm = Depends(), database = Depends(utils.connectDb)):
    cursor = database[1]

    cursor.execute('SELECT * FROM users WHERE username = %s;', (userInfo.username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                            detail=f'Invalid credentials')
    if not utils.verify(userInfo.password, user['password']):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    
    access_token = oauth2.createAccessToken(data={"user_id": user['id']})
    response.set_cookie(httponly=True, key= "acess_token", value=f"bearer {access_token}", samesite='none', secure=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/auth_user')
def authUser(request: Request):
    try:
        token = request.cookies['acess_token'].split()[1]
    except:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                        detail=f'Invalid credentials')
    user = oauth2.getCurrentUser(token)
    return user

@router.get('/log_out', status_code=status.HTTP_200_OK)
def logOut(response: Response):
    response.set_cookie(httponly=True, key= "acess_token", value=None, samesite='none')
    return {'log_out': 'ok'}