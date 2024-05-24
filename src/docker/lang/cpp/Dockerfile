FROM gcc:12.3.0 

COPY . /code-data 

WORKDIR /code-data 

RUN chmod +x /code-data/script.sh 

ENTRYPOINT ["/code-data/script.sh"]