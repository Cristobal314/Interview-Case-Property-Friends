FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt README.md ./ 
COPY src ./src
COPY config ./config

RUN pip install --upgrade pip \ 
    && pip install -r requirements.txt 

ENTRYPOINT [ "property-friends" ]
CMD ["--help"]