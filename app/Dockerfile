FROM python:3.8.3-slim-buster
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "app.py"]