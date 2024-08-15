## Dockerfile

FROM python:3.11.9-slim-bullseye

RUN mkdir golfstore_webcrawler_job

WORKDIR /golfstore_webcrawler_job

COPY . ./

RUN apt-get update -y 

RUN apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y procps
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

RUN pip install -r requirements.txt

RUN chmod -cR 640 *

RUN echo $(pwd)

CMD [ "python","-u","app.py" ]

