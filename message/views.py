from HealthNet.models import Message
from message.forms import MessageForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from HealthNet.models import Log, User
from django.utils import timezone
from django.db.models import Q

def message(request):
    error=False
    user=request.user
    if not user.is_authenticated():
        return redirect('/login')

    if request.method == 'POST':
        messageForm = MessageForm(data=request.POST)
        if messageForm.is_valid():

            userKey=messageForm.getUserKey()
            if userKey != 0:

                message = messageForm.save(commit=False)
                message.sender=user
                message.timeStamp=timezone.now()
                message.receiver=userKey
                message.save()

                log= Log()
                log.user = user
                log.username = request.user.username
                log.time = timezone.now()
                log.type = 'Message'
                log.save()
            else:
                error = True

    else:
        messageForm = MessageForm()

    #unread=Message.objects.filter(receiver=user, read=False)
    #unreadCount=len(unread)
    #unread.update(read=True)
    messages=Message.objects.filter(Q(receiver=user) | Q(sender=user)).order_by('-timeStamp')

    context= {'messageForm': messageForm, 'messages': messages, 'user': User,
              'error': error}
    return context