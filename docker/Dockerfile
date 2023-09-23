FROM python:3.10-slim-bullseye

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y
RUN python3 -m pip install pip --upgrade pip
#Used in Bank Account Monitor
RUN pip install pypdf
#Used unit test code coverage
RUN pip install coverage
#Used as static type checker for Python
RUN pip install mypy
#Used for end to end tests
RUN pip install robotframework
RUN pip install robotframework-debuglibrary
RUN pip install reportlab