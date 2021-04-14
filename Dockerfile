FROM python:3.8.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /root/placasvirtuais
WORKDIR /root/placasvirtuais
COPY requirements.txt /root/placasvirtuais/
EXPOSE 5699
RUN pip install -r requirements.txt
COPY . /root/placasvirtuais/
