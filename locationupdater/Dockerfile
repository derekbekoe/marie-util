FROM python:3.5

RUN pip install gunicorn Flask flask-cors requests pymongo
ADD app.py /
ADD templates /templates
ADD static /static
ENV FLASK_APP app.py

# CMD flask run --port 80 --host 0.0.0.0
CMD gunicorn -w 10 -b 0.0.0.0:80 app:app
