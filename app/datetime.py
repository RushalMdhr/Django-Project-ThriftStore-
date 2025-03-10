from django.utils.timezone import now
import pytz

def get_nepal_time():
    nepal_timezone = pytz.timezone('Asia/Kathmandu')
    return now().astimezone(nepal_timezone)

class YourModel(models.Model):
    date = models.DateTimeField(default=get_nepal_time)
