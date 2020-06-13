FROM python:3.6.2
COPY requirements.txt .
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
COPY . .
CMD python3 manage.py runserver 0.0.0.0:8000