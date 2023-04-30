FROM python:3.11
RUN pip install kopf kubernetes
COPY handlers.py /handlers.py
CMD kopf run --all-namespaces --standalone -v /handlers.py