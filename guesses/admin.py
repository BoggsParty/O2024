from django.contrib import admin
from .models import Guess, Score, EmailReminder, DailyEmail

class EmailReminderAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "subscribe")

admin.site.register(Guess)
admin.site.register(Score)
admin.site.register(EmailReminder, EmailReminderAdmin)
admin.site.register(DailyEmail)
