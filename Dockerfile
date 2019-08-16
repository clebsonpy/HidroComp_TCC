FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn FlowHub.wsgi:application --bind 0.0.0.0:$PORT