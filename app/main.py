from fastapi import FastAPI
from .routers import auth, lessons, subjects
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


origins = ["http://localhost:8080", "https://revisapp.vercel.app"]


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]
app = FastAPI(middleware= middleware)

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins= origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#    expose_headers= ["header1"]
#)

app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(subjects.router)

@app.get('/')
def mengo():
    return {'mengo': 'mengo\nmengo\nmengo\nmengo\nmengo\nmengo\nmengo\nmengo\nmengo'}


