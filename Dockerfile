FROM python:3.6

WORKDIR /microblog
COPY requirements.txt requirements.txt

#RUN python3 -m venv venv
#RUN venv/bin/pip3 install -r requirements.txt
#RUN venv/bin/pip3 install gunicorn

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


COPY app app
COPY microblog.py config.py boot.sh .env ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

EXPOSE 5000
#ENTRYPOINT ["./boot.sh"]