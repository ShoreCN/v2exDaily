FROM ubuntu:latest

MAINTAINER shore<c.shore.cn@gmail.com>


RUN mkdir /app
WORKDIR /app
COPY . /app

# 更新镜像源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse" > /etc/apt/sources.list
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse" >> /etc/apt/sources.list
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse" >>/etc/apt/sources.list
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse" >>/etc/apt/sources.list
RUN sed -i 's/https/http/g' /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y python3.5 --no-install-recommends
RUN ln -s /usr/bin/python3.5 /usr/bin/python
RUN apt-get install -y python3-pip --no-install-recommends
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip

RUN pip install requests
#RUN pip install setuptools
RUN apt-get install -y tesseract-ocr --no-install-recommends
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ setuptools
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ pytesseract
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ lxml
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ beautifulsoup4

# 死循环脚本用以调试
RUN chmod +x /app/run.sh
ENTRYPOINT ["/app/run.sh"] 
