FROM python:3.9.6

RUN mkdir /app_grupo3
WORKDIR /app_grupo3

COPY requirements.txt /app_grupo3/

RUN pip install -r requirements.txt

COPY . /app_grupo3/

ENV RUNNING_IN_DOCKER = True

RUN mkdir /app_grupo3/data

CMD ["python", "organizapp/manage.py", "runserver", "0.0.0.0:8000"]