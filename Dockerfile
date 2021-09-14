FROM python:3.7-slim
ADD requirements.txt /
RUN pip install --upgrade -r /requirements.txt
ADD . /captcha
ENV PYTHONPATH=$PYTHONPATH:/captcha/
WORKDIR /captcha/captcha_validation/services/
EXPOSE 8000
CMD python service.py
