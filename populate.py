from app import db
#from datetime import datetime
from app.models import *

# Add Region
region = Region(code='hk', name='HONG KONG')
db.session.add(region)
region = Region(code='my', name='MALAYSIA')
db.session.add(region)
region = Region(code='sg', name='SINGAPORE')
db.session.add(region)
region = Region(code='th', name='THAILAND')
db.session.add(region)
region = Region(code='ca', name='CANADA')
db.session.add(region)
region = Region(code='us', name='UNITED STATES OF AMERICA')
db.session.add(region)
region = Region(code='cn', name='CHINA')
db.session.add(region)

db.session.commit()