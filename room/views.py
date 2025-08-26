from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Room, Message


@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room).order_by('-id')[:25]
    messages = list(messages)[::-1]  # oldest first for display
    return render(request, 'room/room.html', {'room': room, 'messages': messages})

 
@login_required
def room_messages(request, slug):
    room = get_object_or_404(Room, slug=slug)
    after = int(request.GET.get('after', 0)) if request.GET.get('after', '0').isdigit() else 0
    qs = Message.objects.filter(room=room, id__gt=after).order_by('id')
    data = [
        {
            'id': m.id,
            'content': m.content,
            'username': m.user.username,
            'date': m.date_added.strftime('%H:%M:%S'),
        }
        for m in qs
    ]
    return JsonResponse({'messages': data})


@login_required
@require_http_methods(["POST"])
def create_message(request, slug):
    room = get_object_or_404(Room, slug=slug)
    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'empty'}, status=400)
    msg = Message.objects.create(room=room, user=request.user, content=content)
    return JsonResponse({
        'id': msg.id,
        'content': msg.content,
        'username': msg.user.username,
        'date': msg.date_added.strftime('%H:%M:%S'),
    })