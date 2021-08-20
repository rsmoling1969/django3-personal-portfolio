from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime, time, timedelta
from django.contrib.auth.models import User

# Create your models here.
class CoblentzNumbers(models.Model):
    date = models.DateField(auto_now_add=False)
    class AMorPM(models.TextChoices):
        AM = 'AM', _('AM')
        PM = 'PM', _('PM')

    shift = models.CharField(max_length=2, choices=AMorPM.choices, default=AMorPM.AM)
    numbers = models.CharField(max_length=200) #For now, sadly, a comma delimited list of shift numbers
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return str(self.date) + ' ' + str(self.shift) + ' User: ' + str(self.user)

    def counts_and_averages(self):
        times_and_numbers = {}
        initial_time = 10 if self.shift == self.AMorPM.AM else 16
        minute_start = 0
        if initial_time == 10:
            minute_start = 15
        else:
            minute_start = 45
        myTime = datetime(year=2021,month=7,day=1,hour=initial_time, minute=minute_start, second=0)
        count = 1
        last_number = 0
        for number in self.numbers.split(','):
            try:
                print(f"In try, number is {number}, count is {count}")
                running_average = int(number) / int(count)
                number_in_last_15 = int(number) - last_number
                last_number = int(number)
                print(f"running_average is {running_average}")
            except:
                print(f"Caused an exception")
                running_average = last_number / int(count)
                number_in_last_15 = 0
            times_and_numbers[myTime.strftime("%H:%M")] = [number, number_in_last_15,   running_average]
            print(f"OUR TOTAL ARRAY: {times_and_numbers}")
            myTime += timedelta(minutes=15)
            count += 1
        print(times_and_numbers)
        return times_and_numbers










