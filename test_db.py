from web_app import db
from web_app.models import Users, Devices
from datetime import datetime

u = Users(user_name='Вася', post='бос')
d = Devices(ser_num='2254', app_num='4532-4', modification='мод1', date=datetime.now())


db.session.add(u)
db.session.add(d)
db.session.commit()
