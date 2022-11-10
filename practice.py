from datetime import date, datetime
# today = date.today()
# today_str = today.strftime("%m/%d/%Y")
# print(date.today())

today = "11/9/1a"
ftoday = datetime.strptime(today, '%m/%d/%y')
print(ftoday)