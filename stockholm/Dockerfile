FROM debian:buster

LABEL mainteiner=fballest@student.42madrid.com

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y python3 python3-pip vim

ADD /infection /home/infection
ADD /infection/subcarpeta /home/infection/subcarpeta
ADD /infection/subcarpeta/S1 /home/infection/subcarpeta/S1
ADD /infection/subcarpeta/S2 /home/infection/subcarpeta/S2

COPY ./stockholm.py /stockholm.py
COPY ./README.md /README.md
RUN chmod +x /stockholm.py
RUN python3 -m pip install --user --upgrade setuptools wheel twine
RUN python3 -m pip install markdown
RUN python3 -m pip install pyAesCrypt
RUN python3 -m pip install argparse

# CMD ["python stockholm.py"]
# RUN cp /stockholm.py /stockholm/stockhom.py
