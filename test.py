from datetime import datetime

st_date = "April 17, 2008 11:14:18 PM"

dt_date = datetime.strptime(st_date, "%B %d, %Y %I:%M:%S %p")
print dt_date.strftime("%Y-%m-%d %H:%m:%S")


