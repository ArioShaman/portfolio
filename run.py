#!/usr/bin/env python
from app import app
app.run(debug = True,threaded=True)

from flask.ext.mail import Message
from app import app, mail
