#docker build -t image-custom-controls .
#docker run -w "/usr/local/image_custom_controls" -p 5001:5001 image-custom-controls
FROM python:3.7

LABEL maintainer="M.Selman SEZGİN <mselmansezgin@gmail.com>"

COPY requirements.txt /usr/local/image_custom_controls/requirements.txt

RUN pip3 install -r /usr/local/image_custom_controls/requirements.txt

ADD . /usr/local/image_custom_controls

CMD cd /usr/local/image_custom_controls/controller && python3 /usr/local/image_custom_controls/controller/rest_controller.py