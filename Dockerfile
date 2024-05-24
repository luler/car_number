FROM python:3.6

MAINTAINER 1207032539@qq.com

COPY ./ /root/car_number

WORKDIR /root/car_number

RUN apt-get update && apt-get install -y libgl1-mesa-dev

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 8000

CMD ["python", "api.py"]