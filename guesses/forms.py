from django.forms import ModelForm
from django import forms
from .models import Guess
from sports.models import Sport
from django.shortcuts import get_object_or_404

class TeamGuessForm(forms.ModelForm):

    class Meta:
        model = Guess
        fields = ('gold_country', 'silver_country', 'bronze_country',)

    def __init__(self, *args, **kwargs):
        sport = kwargs.pop('sport')
        sport_query = get_object_or_404(Sport, slug = sport)
        sport_id = sport_query.id
        super(TeamGuessForm, self).__init__(*args, **kwargs)
        self.fields['gold_country'].queryset = self.fields['gold_country'].queryset.filter(sport=sport_id)
        self.fields['silver_country'].queryset = self.fields['silver_country'].queryset.filter(sport=sport_id)
        self.fields['bronze_country'].queryset = self.fields['bronze_country'].queryset.filter(sport=sport_id)
  
class IndividualGuessForm(forms.ModelForm):

    class Meta:
        model = Guess
        fields = ('gold_athlete', 'silver_athlete', 'bronze_athlete',)

    def __init__(self, *args, **kwargs):
        sport = kwargs.pop('sport')
        sport_query = get_object_or_404(Sport, slug = sport)
        sport_id = sport_query.id
        super(IndividualGuessForm, self).__init__(*args, **kwargs)
        self.fields['gold_athlete'].queryset = self.fields['gold_athlete'].queryset.filter(sport=sport_id)
        self.fields['silver_athlete'].queryset = self.fields['silver_athlete'].queryset.filter(sport=sport_id)
        self.fields['bronze_athlete'].queryset = self.fields['bronze_athlete'].queryset.filter(sport=sport_id)

