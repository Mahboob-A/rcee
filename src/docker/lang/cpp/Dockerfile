FROM gcc:12.3.0

COPY . /user-codes/cpp 
WORKDIR /user-codes/cpp

RUN chmod +x /user-codes/cpp/script.sh

ENTRYPOINT ["/user-codes/cpp/script.sh"]