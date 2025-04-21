FROM python:3.7
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY handlers.py /handlers.py
CMD kopf run --all-namespaces --standalone -v /handlers.py