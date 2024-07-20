from django.contrib import admin
from .models import Sport, Athlete, Country, Images
from import_export.admin import ImportExportModelAdmin


class SportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = [
        (
            "About", 
            {
                "classes": ["collapse"],
                "fields": ["sport_name", "slug", "active", "order", "ass_link"],
            },
        ),
        (
            "Participants",
            {
                "classes": ["collapse"],
                "fields": ["team", "country_teams", "athletes"],
            },
        ),
        (
            "Lock Times",
            {
                "classes": ["collapse"],
                "fields": ["locked", "lock_date"],
            },
        ),
        (
            "Winners",
            {
                "fields": ["awarded_date", "awarded", "gold_country", "silver_country", "bronze_country", "gold_athlete", "silver_athlete", "bronze_athlete"],
            },
        ),
    ]
    list_display = ("sport_name", "slug")
    filter_horizontal = ("country_teams","athletes")
    autocomplete_fields = ["gold_country", "silver_country", "bronze_country", "gold_athlete", "silver_athlete", "bronze_athlete"]
    
class AthleteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["athlete"]
    
class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["abbreviation"]
            
admin.site.register(Sport, SportAdmin)
admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Images, ImportExportModelAdmin)
