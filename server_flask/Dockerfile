FROM python:3.8

WORKDIR /app



ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .. .
ADD .env.docker /code/.env

ENTRYPOINT ["python", "app.py"]