from django.contrib import admin
from .models import Guess, Score, EmailReminder, DailyEmail

admin.site.register(Guess)
admin.site.register(Score)
admin.site.register(EmailReminder)
admin.site.register(DailyEmail)
