FROM thinkwhere/gdal-python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn HidroComp_TCC.wsgi:application --bind 0.0.0.0:$PORT