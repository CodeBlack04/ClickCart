from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm

# Create your views here.

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversation = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversation:
        return redirect('conversation:detail', conversation_pk=conversation.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid:
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)    
    else:
        form = ConversationMessageForm()

    return render(request=request, template_name='conversation/new.html', context={
        'form': form,
        'title': 'New Conversation'
    })

@login_required
def inbox(request):

    conversations = Conversation.objects.filter(members__in = [request.user.id])

    return render(request=request, template_name='conversation/inbox.html', context={
        'conversations': conversations,
        'title': 'Inbox'
    })

@login_required
def detail(request, conversation_pk):
    conversation = Conversation.objects.filter(members__in = [request.user.id]).get(pk=conversation_pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid:
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save() #to update the modified_at of conversation

            return redirect('conversation:detail', conversation_pk=conversation_pk)
        

    else:
        form = ConversationMessageForm()

    return render(request=request, template_name='conversation/detail.html', context={
        'conversation': conversation,
        'form': form,
        'title': 'Conversation',
    })