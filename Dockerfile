FROM python:3.11.0 

WORKDIR /usr/src/app 

COPY requirements.txt ./ 

RUN pip install -r requirements.txt 

COPY . .

CMD ["uvicorn", "app.main:app", ,"--reload", "--host", "0.0.0.0", "--port", "8080"]