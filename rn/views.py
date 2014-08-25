import json
import redis
import hashlib
import time
import json as simplejson
import random
import string

from notifications import notify
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from rn.models import User,UserProfile,Player
from rn.forms import ContactForm,LoginForm
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from rn.models import UserDetails,activePlayer, Bidder,UserPurse, Team
from rn.models import UserDetails,activePlayer, Bidder,UserPurse,Team,active
from datetime import datetime
from django.contrib.auth import authenticate, login


active_player=1
num_bidders = 2
@never_cache    
def profile(request):
    if 'session_name' not in request.session:
        return HttpResponseRedirect("home.html")
    return render(request,"profile.html")

def timer_update(request):
    t=Timer.objects.get(t_id=1)
    t.time=int(request.GET['time'])
    t.save()
        
    return HttpResponse("")

def timer(request):
    ob=Timer.objects.get(t_id=1)
    return render(request,"timer.html",{'time':ob.time})

@never_cache   
def login_submit(request):
    email=request.POST['email']
    password=request.POST['password']
    try:
        u=UserDetails.objects.get(email=email,password=password,verified=1)
    except:
        return render(request,"login.html",{'message':"Incorrect Username/password..Also please make sure your account is verified."})
  
    if u:
       up=UserProfile.objects.get(email=u)
       request.session['user_name']=up.first_name+" "+up.last_name  
       request.session['session_name']=u.email
       return profile(request)

def logout(request):
    try:
        del request.session['session_name']
    except:
        pass
    return HttpResponseRedirect("home.html")

def view_browser(request):
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    return render(request,"home.html")

def confirm_signup(request):
    try:
        strid=request.GET['id']
        if not strid:
            return HttpResponse("Wrong URL, dude.")
    except:
        return HttpResponse("Wrong URL,dude.")
    try:
        u=UserDetails.objects.get(hashed=request.GET['id'],verified=0)
        
        if u:
            u.verified=1
            u.save()
            return render(request,"login.html",{'message':"Congratulations.\n\nYour account has been successfully verified.\n\nPlease login to continue."})
            
    except:
        return render(request,"error_signup.html",{'message':"The URL seems to have expired. Register again to start an auction."})

def home(request):
    try:
        r=request.session['session_name']
        if r:
            return render(request,"profile.html")
            
    except:
        pass
    form=ContactForm()
    login_form=LoginForm
    return render(request,"home.html",{'form':form,'login_form':login_form})

def form_search(request):
    form=ContactForm()
    return render(request,'form.html',{'form':form})

def submit_data(request):
    context=RequestContext(request)
    try:
        u=UserDetails.objects.get(email=request.POST['email'])
    
        if u:
            return render(request,"error_signup.html",{'message':"This email address exists. Please provide a different email address."})  
    except:
        pass
    if request.method == 'POST':
        
        
        strid=hashlib.sha224(request.POST['email']).hexdigest()
        mail_title = 'Welcome to IPL Auctions 2015.'
        message = 'Hello %s,\n\n Welcome to IPL Auctions 2015. We are glad to have you here.\n\n Follow the link below to activate your account and start your league.\n\nhttp://127.0.0.1:8000/confirm_signup?id=%s\n\nThanks.\nIndian Premiere League.' %(request.POST['first_name'],strid)
        email = 'admin@ipl.com'
        recipients = request.POST['email']

        send_mail(mail_title, message, email, [recipients])
        email=request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password=request.POST['password']
        age=int(request.POST['age'])
        gender=request.POST['gender']
        u=UserDetails(email=email,password=password,hashed=strid,verified=0)
        u.save()
        u=UserDetails.objects.get(email=email)
        up=UserProfile(email=u,first_name=first_name,last_name=last_name,age=age,gender=gender)
        up.save()
        return render(request,"success.html")
            
    else:
        return HttpResponse("The form is invalid")




@never_cache   
def login_check(request):
    if request.method!='POST':
        form=ContactForm()
        login_form=LoginForm()
        return render(request,"home.html",{'form':form,'login_form':login_form})
    else:
        name=request.POST['name']
        password=request.POST['password']

def search_this(request):

    if 'q' in request.POST:
        q=request.POST['q']
        user=UserDetails.objects.filter(name__icontains=q)
        return render(request,'display_results.html',{'user':user,'query':q})
        
    else:
        return render(request,'display_results.html',{'error':True})
        
    return HttpResponse(message)

def auc_screen(request):
    context  = RequestContext(request)
    player_list = Player.objects.all()
    context_dict = {'player_list': player_list}
    return render_to_response('auc_screen.html', context_dict, context)

def detail(request, player_id):
    notifications = request.user.notifications.unread().order_by('-timestamp')
    uob=User.objects.get(username=request.user)
    aob=active.objects.get(aid=1)
    player_id=aob.active_player
    ob=UserPurse.objects.get(user_data=uob)
    if ob.deactivated==1:
        return render(request, 'auction_over.html', {'ob':ob})

    player = Player.objects.get(pk=player_id)
    
    return render(request, 'detail.html', {'player':player,'notifications':notifications,'money':ob.money, 'ob':ob})


def update_player(request):
    notifications = request.user.notifications.unread().order_by('-timestamp')
    recipients = User.objects.all()
    pid=int(request.POST['pId'])
    pBid=int(request.POST['pBid'])

    

    # ob=pBidModel.objects.get(pId=pid)
    pob=Player.objects.get(pk=pid)
    if pob.pAuctioned==1:
        return HttpResponse(json.dumps({"success":False}),content_type="application/json")

    else:



        if pob.pBaseprice==pBid:
            pass

        else:

            for notification in notifications:
                p=notification.actor.pk
                uob=User.objects.get(pk=p)
                ob=UserPurse.objects.get(user_data=uob)
                ob.money=ob.money-pBid
                ob.playersBought+=1
                if(pob.pCountry!="India"):
                    ob.playersForeign+=1
                ob.playersList=ob.playersList+pob.pName+", "
                ob.save()
                pob.pTeam=notification.actor
                pob.pBid=pBid
                pob.pStatus='Sold'
                break
        pob.pAuctioned=1
        pob.save()

        aob=active.objects.get(aid=1)
        aob.active_player=pid+1
        aob.save()
    

        for recipient in recipients:
            notify.send(
                request.user,
                recipient=recipient,
                verb="Player Sold."

    
            
            

            )

        return HttpResponse(json.dumps({"success":True}),content_type="application/json")    

@login_required
def home_realtime(request):
    notifications = request.user.notifications.unread().order_by('-timestamp')
    ob=Timer.objects.get(t_id=1)
    tob=Notification.objects.all()
    for  t in tob:
        timer=t.timestamp
        break
    timer= time.mktime(timer.timetuple())
    timer=timer%(60)

    return render(request, 'index_realtime.html', {'notifications': notifications,'timer':timer})

def update_bid(request):
    user=request.user
    return render(request,"update_bid.html",{'user':user})

def raise_bid(request):
    return HttpResponse(request,{'value':1000})

def timer_update(request):
    
    t=Timer.objects.get(t_id=1)
    t.time=int(request.GET['time'])
    t.save()
        
    return HttpResponse("")
    
    
def treset(request):
    if request.is_ajax():
        ob=Timer.objects.get(t_id=1)
        ob.time=int(request.GET['time'])
        ob.save()
    return HttpResponse("") 



def send_notification(request):
    
    recipients = User.objects.all()

    for recipient in recipients:
        notify.send(
            request.user,
            recipient=recipient,
            verb="Bid Raised."
        )

    return HttpResponse(json.dumps({"success": True}), content_type="application/json")


@login_required
def ajax_send_notification(request):
    
    pid=int(request.POST['pId'])
    pob=Player.objects.get(pk=pid)
    if pob.pBid==0:
        pob.pBid=pob.pBaseprice+1000000
    else:
        pob.pBid=pob.pBid+1000000

    pob.save()
    recipients = User.objects.all()
    
    

    for recipient in recipients:
        notify.send(
            request.user,
            recipient=recipient,
            verb=pob.pBid
            
            

        )

    return HttpResponse(json.dumps({"success": True}), content_type="application/json")


@login_required
def ajax_mark_as_read(request):
    request.user.notifications.unread().mark_all_as_read()

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    for session in request.user.session_set.all():
        redis_client.publish(
            'notifications.%s' % session.session_key,
            json.dumps({"mark_as_read": True, "unread_count": 0})
        )

    return HttpResponse(json.dumps({"success": True}), content_type="application/json")




@receiver(post_save, sender=Notification)
def notification_post_save(sender, **kwargs):
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    notification = kwargs['instance']
    recipient = notification.recipient

    
    for session in recipient.session_set.all():
        redis_client.publish(
            'notifications.%s' % session.session_key,
            json.dumps(
                dict(
                    timestamp=notification.timestamp.isoformat(),
                    recipient=notification.recipient.username,
                    actor=notification.actor.username,
                    verb=notification.verb,
                    action_object=notification.action_object,
                    target=notification.target,
                    description=notification.description
                    
                )
            )
        )

def setup(request):
    if request.method == 'POST':
        for i in range(num_bidders):
            num_id = 'id'+str(i+1)
            recipient = request.POST[num_id]
            #strid=hashlib.sha224(recipient).hexdigest()
            strid = recipient
            mail_title = 'Signup for auction'
            message = 'Please click on the following link to signup for the auction: \nhttp://127.0.0.1:8000/bidder_signup?id=%s '%(strid)
            email = 'admin@ipl.com'
            list_recipients = [recipient]
            send_mail(mail_title, message, email, list_recipients)
        return render(request, "profile.html") 

    else:
        return render(request, "setup.html")

def bidder_signup(request):
    if request.method == 'GET':
        strid = request.GET['id']
        request.session["email"] = strid
        return render(request, "bidder_signup.html")

    elif request.method == 'POST':
        fname = request.POST["first_name"]
        lname = request.POST["last_name"]
        uname = request.POST["username"]
        passwd = request.POST["password"]
        b = User.objects.create_user(username=uname, email=request.session["email"], first_name=fname, last_name=lname, password=passwd)
        return HttpResponseRedirect("usr_login.html")



def select_team(request):
    if request.method == 'POST':
        try:
            Team.objects.get(name= request.POST["team"])
            return render(request, "select_teams.html")

        except:
            username=request.POST['team']

            
            b = User.objects.get(username=request.user)
            Team.objects.create(name=request.POST["team"], owner = b.username)
            pob=UserPurse(money=600000000,user_data=b)
            pob.save()
            return HttpResponseRedirect("auction_start.html")
    else:
        return render(request, "select_teams.html")

def auction_start(request):
    return render(request, "auction_start.html")

def usr_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("select_teams.html?un="+username)
            else:
                return render(request, "usr_login.html")
        else:
            return render(request, "usr_login.html")
    else:
        return render(request, "usr_login.html")

def bidder_quit(request):
    if request.method=='POST':
        uid=User.objects.get(username=request.user)
        pid=UserPurse.objects.get(user_data=uid)
        pid.deactivated=1
        pid.save()
        return HttpResponse("")
    if request.method=='GET':
        uid=User.objects.get(username=request.user)
        pid=UserPurse.objects.get(user_data=uid)
        if pid.deactivated==1:
            return render(request, "auction_over.html", {'ob':pid})
    return HttpResponse("NNJMGHJ")