#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
import atexit
from flask import Flask, request, make_response
from captcha_validation.config.Config import Config
from captcha_validation.business.CaptchaBusiness import CaptchaBusiness
from captcha_validation.utils.InitializeSQLite import InitializeSQLite
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

log_level = Config().get_log_level()
log = logging.getLogger(__name__)
log.setLevel(getattr(logging, log_level))



@app.route('/get_captcha', methods=['GET'])
def get_captcha():
    log.info(f"ip: {request.remote_addr} method: {request.method}")
    bus = CaptchaBusiness()
    captcha = bus.generate_captcha(address=request.remote_addr)
    if not captcha.case:
        return captcha.message,500
    response = make_response(captcha.message.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=captcha_validation.jpeg'
    response.mimetype = 'image/jpeg'
    return response

@app.route('/validate_captcha', methods=['POST'])
def validate_captcha():
    log.info(f"ip: {request.remote_addr} method: {request.method}")
    argz_data = request.get_json()
    solution = argz_data['solution']
    address = request.remote_addr
    bus = CaptchaBusiness()
    validate = bus.validate_captcha(solution, address)
    if not validate.case:
        return validate.message,400
    return validate.message,200

def initialize_sqlite():
    log.info("Starting scheduled task. Trying to remove records older than 3 minutes")
    db_init = InitializeSQLite()
    db_init.run()

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(id = 'Remove records older than 3 minutes', func = initialize_sqlite ,trigger="interval", seconds=30)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run(debug=False, port=8000, host='0.0.0.0')