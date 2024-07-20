from django.db import models
from django.contrib.auth.models import User
from sports.models import Sport, Athlete, Country

class Guess(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name = 'user+')
    sport = models.ForeignKey('sports.Sport', models.SET_NULL, blank=True, null=True, related_name = 'sport+')
    score = models.IntegerField(default=0)
    
    gold_athlete = models.ForeignKey('sports.Athlete',  models.SET_NULL, blank=True, null=True, related_name = 'ga+')
    silver_athlete = models.ForeignKey('sports.Athlete',  models.SET_NULL, blank=True, null=True, related_name = 'sa+')
    bronze_athlete = models.ForeignKey('sports.Athlete',  models.SET_NULL, blank=True, null=True, related_name = 'ba+')
    
    gold_country = models.ForeignKey('sports.Country',  models.SET_NULL, blank=True, null=True, related_name = 'gc+')
    silver_country = models.ForeignKey('sports.Country',  models.SET_NULL, blank=True, null=True, related_name = 'sc+')
    bronze_country = models.ForeignKey('sports.Country',  models.SET_NULL, blank=True, null=True, related_name = 'bc+')

    def __str__(self):
        return str(self.sport)
        
    class Meta:
        verbose_name = "Guess"
        verbose_name_plural = "Guesses"
        
class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=False)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user)
        
    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        
class EmailReminder(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=False)
    subscribe = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True, unique=True)
    
    def __str__(self):
        return str(self.user)
        
    class Meta:
        verbose_name = "Email Reminder"
        verbose_name_plural = "Email Reminders"
        
class DailyEmail(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    sent = models.BooleanField(default=False)
    sports_txt = models.TextField(blank=True)
    sports_html = models.TextField(blank=True)
    email_txt = models.TextField(blank=True)
    email_html = models.TextField(blank=True)
    
    def __str__(self):
        return str(self.date)
    