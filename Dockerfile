FROM python:3.6

WORKDIR /microblog

RUN apt-get update && apt-get -y install cron

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .

ENV FLASK_APP microblog.py
EXPOSE 5000

COPY cron_command /etc/cron.d/cron_command
RUN chmod 0644 /etc/cron.d/cron_command
RUN chmod +x cron_bash.sh
RUN chmod 0744 cron_job_script.py
RUN crontab /etc/cron.d/cron_command

COPY .env .env

CMD cron

#RUN chmod +x boot.sh
#ENTRYPOINT ["./boot.sh"]
