FROM python:3.5
WORKDIR /wts/
ADD requirements.txt /wts/requirements.txt
RUN pip install -r requirements.txt
ADD . /wts/
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
