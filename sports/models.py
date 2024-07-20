from django.db import models

 
class Sport(models.Model):
    sport_name = models.CharField(max_length=200, default='')
    slug = models.SlugField(max_length=50, default='')
    order = models.IntegerField(default=100)
    active = models.BooleanField(default=False)
    ass_link = models.URLField(max_length=200, blank=True, help_text="The official website of sports international governing body.")
   
    team = models.BooleanField(default=True)
    country_teams = models.ManyToManyField('sports.Country', blank=True)
    athletes = models.ManyToManyField('sports.Athlete', blank=True)
    
    locked = models.BooleanField(default=False)
    awarded = models.BooleanField(default=False)
    lock_date = models.DateField(blank=True)
    awarded_date = models.DateField(blank=True)
    
    gold_country = models.ForeignKey('sports.Country', models.SET_NULL, blank=True, null=True, related_name = 'gc')
    silver_country = models.ForeignKey('sports.Country', models.SET_NULL, blank=True, null=True, related_name = 'sc')
    bronze_country = models.ForeignKey('sports.Country', models.SET_NULL, blank=True, null=True, related_name = 'bc')
    
    gold_athlete = models.ForeignKey('sports.Athlete', models.SET_NULL, blank=True, null=True, related_name = 'ga')
    silver_athlete = models.ForeignKey('sports.Athlete', models.SET_NULL, blank=True, null=True, related_name = 'sa')
    bronze_athlete = models.ForeignKey('sports.Athlete', models.SET_NULL, blank=True, null=True, related_name = 'ba')
    
    def __str__(self):
        return self.sport_name
        
class Athlete(models.Model):
    athlete = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.athlete
    
class Country(models.Model):
    numeric_code = models.IntegerField()
    full_name = models.CharField(max_length=200, default='')
    abbreviation = models.CharField(max_length=3, default='', help_text="Alpha-3")
    
    def __str__(self):
        return self.abbreviation
        
    class Meta:
        verbose_name = "County"
        verbose_name_plural = "Countries"
        
class Images(models.Model):
    sport = models.OneToOneField('sports.Sport', on_delete=models.CASCADE, parent_link=False)
    icon = models.ImageField(blank=True)
    picture = models.ImageField(blank=True)
    
    def __str__(self):
        return str(self.sport)
        
    class Meta:
        verbose_name = "Images"
        verbose_name_plural = "Images" 