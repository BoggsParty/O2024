from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Sum
from .models import Guess, Score
from sports.models import Sport, Images
from .forms import TeamGuessForm, IndividualGuessForm
from django.utils import timezone

def calculate(request):
    success = True
    now = timezone.localtime(timezone.now())
    lock_sports = Sport.objects.exclude(locked=True).filter(lock_date__lt=now)
    lock_sports.update(locked=True)

    active_sport = Sport.objects.filter(awarded=True, active=True)
    
    for sport in active_sport:
        active_user = User.objects.all()
        if sport.team:
            winner_gold = sport.gold_country
            winner_silver = sport.silver_country
            winner_bronze = sport.bronze_country
        else:
            winner_gold = sport.gold_athlete
            winner_silver = sport.silver_athlete
            winner_bronze = sport.bronze_athlete
        for user in active_user:
            score = 0
            
            #fully correct
            if sport.team:
                gold_correct = Guess.objects.filter(user=user, sport=sport, gold_country=winner_gold).count()
                silver_correct = Guess.objects.filter(user=user, sport=sport, silver_country=winner_silver).count()
                bronze_correct = Guess.objects.filter(user=user, sport=sport, bronze_country=winner_bronze).count()
           
            else:
                gold_correct = Guess.objects.filter(user=user, sport=sport, gold_athlete=winner_gold).count()
                silver_correct = Guess.objects.filter(user=user, sport=sport, silver_athlete=winner_silver).count()
                bronze_correct = Guess.objects.filter(user=user, sport=sport, bronze_athlete=winner_bronze).count()
            correct = gold_correct + silver_correct + bronze_correct
            if correct == 1:
                score = 10
            elif correct == 2:
                score = 25
            elif correct == 3:
                score = 50
            else:
                score = 0
            #print (score)
            
            #partially correct
            if sport.team: 
                gold_partial_silver = Guess.objects.filter(user=user, sport=sport, silver_country=winner_gold).count()
                gold_partial_bronze = Guess.objects.filter(user=user, sport=sport, bronze_country=winner_gold).count()
                silver_partial_gold = Guess.objects.filter(user=user, sport=sport, gold_country=winner_silver).count()
                silver_partial_bronze = Guess.objects.filter(user=user, sport=sport, bronze_country=winner_silver).count()
                bronze_partial_gold = Guess.objects.filter(user=user, sport=sport, gold_country=winner_bronze).count()
                bronze_partial_silver = Guess.objects.filter(user=user, sport=sport, silver_country=winner_bronze).count()
            else:
                gold_partial_silver = Guess.objects.filter(user=user, sport=sport, silver_athlete=winner_gold).count()
                gold_partial_bronze = Guess.objects.filter(user=user, sport=sport, bronze_athlete=winner_gold).count()
                silver_partial_gold = Guess.objects.filter(user=user, sport=sport, gold_athlete=winner_silver).count()
                silver_partial_bronze = Guess.objects.filter(user=user, sport=sport, bronze_athlete=winner_silver).count()
                bronze_partial_gold = Guess.objects.filter(user=user, sport=sport, gold_athlete=winner_bronze).count()
                bronze_partial_silver = Guess.objects.filter(user=user, sport=sport, silver_athlete=winner_bronze).count()
            
            partial = gold_partial_silver + gold_partial_bronze + silver_partial_gold + silver_partial_bronze + bronze_partial_gold + bronze_partial_silver
            score = score + (partial*5)
            
            #print (partial)
            
            try:
                guess_score = Guess.objects.get(user=user, sport=sport)
            except: 
                continue
            guess_score.score = score
            #print (guess_score.score)
            guess_score.save()
    
    user_total = User.objects.all()
    for user in user_total:
        total_score = Guess.objects.filter(user=user).aggregate(Sum('score'))
        user_score = Score.objects.get(user=user)
        score_number = total_score['score__sum']
        if score_number != None:
            user_score.score = score_number
            print(user, score_number)
            user_score.save()
        else:
            #print(user,'0')
            continue
            
    return render(request, 'guesses/calculate.html', {"success":success})
    
@login_required()
def all_guesses(request):
    show_logout = True
    
    open_team_guesses = Guess.objects.filter(user = request.user).filter(sport__locked=False).filter(sport__team=True).order_by('sport__order')
    locked_team_guesses = Guess.objects.filter(user = request.user).filter(sport__locked=True).filter(sport__team=True).order_by('sport__order')
    open_individual_guesses = Guess.objects.filter(user = request.user).filter(sport__locked=False).filter(sport__team=False).order_by('sport__order')
    locked_individual_guesses = Guess.objects.filter(user = request.user).filter(sport__locked=True).filter(sport__team=False).order_by('sport__order')
    print(open_team_guesses)
    try:
        locked_team_sport = Sport.objects.filter(locked=True).first()
    except:
        locked_team_sport = None
    
    try:
        locked_individual_sport = Sport.objects.filter(locked=True).first()
    except:
        locked_individual_sport = None
   
    if None not in (locked_individual_sport, locked_team_sport):
        if locked_team_sport.order > locked_individual_sport.order:
            all_guesses_sport = locked_individual_sport
        else: 
            all_guesses_sport = locked_team_sport
    elif locked_individual_sport == None:
        all_guesses_sport = locked_team_sport
    else:
        all_guesses_sport = locked_individual_sport
        
    return render(request,'guesses/guesses.html', {'show_logout':show_logout, 'open_team_guesses':open_team_guesses,'open_individual_guesses':open_individual_guesses,'locked_team_guesses':locked_team_guesses,'locked_individual_guesses':locked_individual_guesses,'all_guesses_sport':all_guesses_sport})
  
@login_required()  
def everyones_guesses(request, sport):
    show_logout = True
    
    sport_query = Sport.objects.get(slug = sport)
    locked_team = Sport.objects.filter(team=True).filter(locked=True).order_by('order')
    locked_individual = Sport.objects.filter(team=False).filter(locked=True).order_by('order')
    guesses = Guess.objects.filter(sport = sport_query).exclude(user = request.user).order_by('score')
    users_guess = Guess.objects.filter(user = request.user).filter(sport = sport_query).first()

    return render(request, 'guesses/all-users.html', {'show_logout':show_logout,'sport_query':sport_query,'locked_team':locked_team,'locked_individual':locked_individual,'guesses':guesses,'users_guess':users_guess,})
    
@login_required()
def quick_guess(request, sport):
    show_logout = True

    sport_query = Sport.objects.get(slug = sport)
    sport_list = Sport.objects.filter(locked=False).order_by('order')
    active_guess = Guess.objects.filter(user = request.user).filter(sport = sport_query).first()
    domain = get_current_site(request).domain
    url = "http://"+domain+"/guesses/edit/all/"+str(sport_query.slug)+"/"
    print(url)
        
    try:
        instance = Guess.objects.filter(user = request.user).filter(sport = sport_query).first()
    except:
        instance = None
        
    if instance:
        if request.method == "POST":
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)
            if form.is_valid():
                guess = form.save(commit=False)
                guess.user = request.user
                guess.sport = sport_query
                guess.save()
                form.save_m2m()
                return redirect(url)
        else:
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)   
            
    else:
        if request.method == "POST":
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)
            if form.is_valid():
                guess = form.save(commit=False)
                guess.user = request.user
                guess.sport = sport_query
                guess.save()
                form.save_m2m()
                return redirect(url)
        else:
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)   
    
    return render(request, 'guesses/quick_guess.html', {'show_logout':show_logout,'sport_list':sport_list,'active_guess':active_guess,'sport_query':sport_query,'form':form,})

@login_required()
def edit(request, sport):
    show_logout = True

    sport_query = Sport.objects.get(slug = sport)
    active_guess = Guess.objects.filter(user = request.user).filter(sport = sport_query).first()
    images = Images.objects.get(sport = sport_query)
    
    try:
        instance = Guess.objects.filter(user = request.user).filter(sport = sport_query).first()
    except:
        instance = None
        
    if instance:
        if request.method == "POST":
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)
            if form.is_valid():
                guess = form.save(commit=False)
                guess.user = request.user
                guess.sport = sport_query
                guess.save()
                form.save_m2m()
                return redirect ("/guesses/all/")

        else:
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)            
    else:
        if request.method == "POST":
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)            
            if form.is_valid():
                guess = form.save(commit=False)
                guess.user = request.user
                guess.sport = sport_query
                guess.save()
                form.save_m2m()
                return redirect ("/guesses/all/")

        else:
            if sport_query.team:
                form = TeamGuessForm(request.POST, sport=sport, instance=instance)
            else:
                form = IndividualGuessForm(request.POST, sport=sport, instance=instance)
    
    return render(request, 'guesses/edit.html', {'show_logout':show_logout, 'images':images,'form':form,'sport_query':sport_query,'active_guess':active_guess,})