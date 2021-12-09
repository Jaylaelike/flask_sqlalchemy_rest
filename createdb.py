# from app import db
# db.create_all()
# exit()

from pytz import timezone
from datetime import datetime
import datetime

UTC = timezone('Asia/Bangkok')
tz = datetime.datetime.now


# x = datetime.now(UTC) 

# print(UTC)
# print(x)
print(tz)
   
