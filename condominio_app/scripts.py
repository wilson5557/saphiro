from datetime import datetime, timedelta


startdate = datetime.today()
enddate = startdate + timedelta(days=6)
noti = Noticia.objects.filter(date__range=[startdate, enddate])

print(noti)