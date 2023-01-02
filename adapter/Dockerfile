FROM python:3.8

RUN pip3 install --upgrade pip
RUN pip3 install paho-mqtt
RUN pip3 install influxdb-client
RUN apt-get update && apt-get install -y netcat

COPY *.py start_script.sh /adapter/

WORKDIR /adapter/

RUN chmod u+x ./start_script.sh

CMD ["./start_script.sh"]
