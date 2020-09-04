FROM python:latest
MAINTAINER mateusz

WORKDIR /home

ADD src/python-movie-collection-checker/get-list-of-movies.py get-list-of-movies.py
RUN chmod 777 get-list-of-movies.py
RUN python3 -m pip install requests

ENTRYPOINT python3 /home/get-list-of-movies.py
