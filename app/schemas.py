from pydantic import BaseModel



class AddSubject(BaseModel):
    subject: str

class DeleteSubjects(BaseModel):
    subjects: list

class AddLesson(BaseModel):
    revision_dates: str | None
    first_rev_date: str | None
    last_rev_date: str | None
    date: str
    chosen_subject: str
    lesson: str

class DeleteLesson(BaseModel):
    ids: list

class GetLast11Revisions(BaseModel):
    dates: list

class CreateUser(BaseModel):
    username: str
    password: str

class CreateUserOut(BaseModel):
    id: int
    username: str
