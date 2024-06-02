FROM python:3.10-slim-bullseye

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y
RUN python3 -m pip install pip --upgrade pip
#Used in Bank Account Monitor
RUN pip install pypdf==4.2.0
#Used unit test code coverage
RUN pip install coverage==7.5.3
#Used as static type checker for Python
RUN pip install mypy==1.10.0
#Used for pie chart presenter
RUN pip install matplotlib==3.9.0
#Used for end to end tests
RUN pip install robotframework==7.0
RUN pip install robotframework-debuglibrary==2.5.0
RUN pip install reportlab==4.2.0
