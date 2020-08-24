FROM docker.esf.fangdd.net/python:3.6.2
COPY requirements.txt .
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
COPY . .
CMD ./start.sh