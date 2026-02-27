#Data
from datetime import date, timedelta
current_data=date.today()
tomorrow=current_data + timedelta(days=1)
yesterday=current_data - timedelta(days=1)
print("Yesterday Date", current_data)
print("Tomorrow", tomorrow)
print("Yesterday", yesterday)

#Day
from datetime import date, timedelta
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday.strftime("%A"))
print("Today:", today.strftime("%A"))
print("Tomorrow:", tomorrow.strftime("%A"))