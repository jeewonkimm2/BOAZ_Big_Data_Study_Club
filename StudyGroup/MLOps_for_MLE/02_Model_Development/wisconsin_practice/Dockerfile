FROM amd64/python:3.9-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

RUN pip install -U pip &&\
    pip install scikit-learn pandas psycopg2-binary

COPY wisconsin_generator.py wisconsin_generator.py

ENTRYPOINT ["python", "wisconsin_generator.py", "--db-host"]
# Change CMD to solve host finding error
CMD ["localhost"]
