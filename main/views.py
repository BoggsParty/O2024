from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import Concat
from django.db.models import TextField, CharField, Value as V
from django.contrib.auth.models import User
from sports.models import Sport
from guesses.models import Score, Guess, EmailReminder, DailyEmail
from django.conf import settings
from magic_link.models import MagicLink
from .forms import Edit_SettingsForm, SignUpForm, LoginEmailForm, EmailReminderForm, EmailNoThankYouForm

#account registration etc. --------------------------------
def logout(request):
    show_logout = False
    return render(request, 'registration/logout.html', {'show_logout':show_logout})
    
def existing_account(request):
    return render(request, 'registration/existing_account.html')
    
def two_accounts(request):
    user = request.user
    send_mail(
        "Two accounts",
        str(user)+" has 2 accounts",
        None,
        ['julia.kuzel@gmail.com'],
        fail_silently=False,
    )
    return render(request, 'registration/two_accounts.html')    
    
def register(request):    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email != '':
                if EmailReminder.objects.filter(email=email).exists():
                    return redirect('existing_account')
                else:
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    #creates score record
                    score = Score()
                    score.user = request.user
                    score.score = 0
                    score.save()  
                    #creates email reminder
                    email_reminder = EmailReminder()
                    email_reminder.user = request.user
                    email_reminder.email = user.email
                    email_reminder.save()
                    #creates blank guesses
                    sport_query = Sport.objects.filter(active = True)
                    for sport in sport_query:
                        guess = Guess()
                        guess.user = request.user
                        guess.sport = sport
                        guess.score = 0
                        guess.save()
                    return redirect('settings')
            else:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                #creates score record
                score = Score()
                score.user = request.user
                score.score = 0
                score.save()  
                #creates email reminder
                email_reminder = EmailReminder()
                email_reminder.user = request.user
                email_reminder.email = None
                email_reminder.save()
                #creates blank guesses
                sport_query = Sport.objects.filter(active = True)
                for sport in sport_query:
                    guess = Guess()
                    guess.user = request.user
                    guess.sport = sport
                    guess.score = 0
                    guess.save()        
                
            
                return redirect('settings')
    else:
        form = SignUpForm()            
    
    return render(request, 'registration/createaccount.html', {'form': form})

def request_link(request):
    if request.method == "POST":
        form = LoginEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user_email = EmailReminder.objects.get(email=email)
                user = User.objects.get(id=user_email.user.id)
                link = MagicLink.objects.create(user=user)
                url = get_current_site(request).domain
                email_body = "Hello, "+user.username+".\r\nPlease use this link to login to your account: http://"+url+"/magic_link/"+str(link.token)+"/ \r\nIf you did not request this link, please reply back to this email."
                send_mail (
                    'Login Link',
                    email_body,
                    None,
                    [user_email.email],
                    fail_silently=False,
                )
            except ObjectDoesNotExist:
                pass
                
            return (render(request, 'registration/login_link_success.html',))
    else:
        form = LoginEmailForm()
    return (render(request, 'registration/login_link.html', {"form": form}))
    
@login_required()
def settings(request):
    show_logout = True
    
    edit_user = request.user
    subscribe = EmailReminder.objects.get(user = request.user)
    
    if request.method == "POST":
        form = Edit_SettingsForm(request.POST,request.FILES, instance=edit_user)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.save()
            return redirect('settings_success')
    else:
        form = Edit_SettingsForm(instance=edit_user)
    return render(request, 'registration/settings.html', {'show_logout':show_logout,'edit_user':edit_user,'form':form,'subscribe':subscribe})
    
@login_required()
def settings_success(request):
    show_logout = True
    
    edit_user = request.user
    subscribe = EmailReminder.objects.get(user = request.user)
    
    if request.method == "POST":
        form = Edit_SettingsForm(request.POST,request.FILES, instance=edit_user)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.save()
            return redirect('settings_success')
    else:
        form = Edit_SettingsForm(instance=edit_user)
    return render(request, 'registration/settings-success.html', {'show_logout':show_logout,'edit_user':edit_user,'form':form,'subscribe':subscribe})

@login_required()
def email_settings(request):
    show_logout = True
    
    edit_user = request.user
    subscribe = EmailReminder.objects.get(user = edit_user)
    
    if request.method == "POST":
        form = EmailReminderForm(request.POST,request.FILES, instance = subscribe)
        if form.is_valid():
            email_settings = form.save(commit=False)
            email_settings.save()
            return redirect('settings_success')
        else:
            return redirect('two_accounts')
    else:
        form = EmailReminderForm(instance=subscribe)
    return render(request, 'registration/settings-email.html', {'show_logout':show_logout,'edit_user':edit_user,'form':form,'subscribe':subscribe})

def test(request):
    if request.user.is_anonymous:
        show_logout = False
        show_subscribe_message = False
        form = None
    else:
        show_logout = True

    edit_user = request.user
    subscribe = EmailReminder.objects.get(user = edit_user)
    
    if subscribe.NTY:
        show_subscribe_message = False
        form = None
    elif subscribe.subscribe:
        show_subscribe_message = False
        form = None
    else:
        show_subscribe_message = True
        if request.method == "POST":
            form = EmailNoThankYouForm(request.POST,request.FILES, instance = subscribe)
            if form.is_valid():
                email_settings = form.save(commit=False)
                email_settings.NTY = True
                email_settings.save()
                return redirect('home')
        else:
            form = EmailNoThankYouForm(instance=subscribe)
            
    return render(request, 'registration/test.html', {'form':form,'show_logout':show_logout,'show_subscribe_message':show_subscribe_message})


# main pages that do not require login. See guess views for the rest of the site ---------------------------

def home(request):
    if request.user.is_anonymous:
        show_logout = False
        show_subscribe_message = False
        form = None
    else:
        show_logout = True
        edit_user = request.user
        subscribe = EmailReminder.objects.get(user = edit_user)
    
        if subscribe.NTY:
            show_subscribe_message = False
            form = None
        elif subscribe.subscribe:
            show_subscribe_message = False
            form = None
        else:
            show_subscribe_message = True
            if request.method == "POST":
                form = EmailNoThankYouForm(request.POST,request.FILES, instance = subscribe)
                if form.is_valid():
                    email_settings = form.save(commit=False)
                    email_settings.NTY = True
                    email_settings.save()
                return redirect('home')
            else:
                form = EmailNoThankYouForm(instance=subscribe)
        
    scores = Score.objects.all().order_by('-score')

    return render(request,'pages/home.html', {'scores':scores,'show_logout':show_logout,'show_subscribe_message':show_subscribe_message,'form':form,})
    
def sports_menu(request):
    if request.user.is_anonymous:
        show_logout = False
    else:
        show_logout = True
        
    team_sports = Sport.objects.filter(active=True).filter(team=True).order_by('order')
    individual_sports = Sport.objects.filter(active=True).filter(team=False).order_by('order')
    
    return render(request, 'pages/sport_menu.html', {'team_sports':team_sports, 'individual_sports':individual_sports, 'show_logout':show_logout})

def about(request):
    if request.user.is_anonymous:
        show_logout = False
    else:
        show_logout = True
        
    return render(request, 'pages/about.html', {'show_logout':show_logout})

def email(request):
    users = EmailReminder.objects.filter(subscribe=True)
    today = timezone.now()
    email_content = DailyEmail.objects.get(date = today)
    if email_content.sent:
        success = False
    else:
        success = True
        for users in users:
            current_user = User.objects.get(id=users.user.id)
            score = Score.objects.get(user=current_user)
        
            subject, from_email, to = "Your Daily Update", None, users.email
            text_content = email_content.sports_txt+"\r\n"+email_content.email_txt
            html_content = email_content.sports_html+email_content.email_html
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        email_content.sent = True
        email_content.save()
    return (render(request, 'guesses/calculate.html', {'success':success}))