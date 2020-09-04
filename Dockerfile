FROM python:latest
MAINTAINER mateusz

# ENV TERM=xterm
ENV TERM=xterm-256color
WORKDIR /home
VOLUME /home/output

RUN python3 -m pip install requests

ADD src/python-movie-collection-checker/get-list-of-movies.py get-list-of-movies.py
RUN chmod 777 get-list-of-movies.py

ENTRYPOINT python3 /home/get-list-of-movies.py
