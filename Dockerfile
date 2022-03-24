FROM python:3.9

WORKDIR /config
COPY ./mercury_exporter_agent.py ./requirements.txt /config/
RUN pip3 install -r requirements.txt
ENV PORT=3000

CMD "python3" "mercury_exporter_agent.py" "$mercury_rpc"
