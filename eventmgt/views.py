from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import date
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q, Count, Max, Min, Avg
from eventmgt.models import Event, Participants, Category
from eventmgt.forms import EventModelForm, CategoryModelForm, ParticipantModelForm

def home_view(request):
    query = request.GET.get('q', '')
    events = Event.objects.all()
    if query:
        events = events.filter(name__icontains=query)
        
    participants = Participants.objects.annotate(event_count=Count('event')).order_by('-event_count')

    context = {
        "events": events,
        "participants": participants
    }
    return render(request, 'landing.html', context)

def organizer_dashboard(request):
    today = now().date()
    event_type = request.GET.get("type", "today")  # Default to "today"

    # Get event counts
    total_participants = Participants.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    participants = Participants.objects.annotate(event_count=Count('event'))
    # Filter events based on selected type
    if event_type == "today":
        events = Event.objects.filter(date=today)  # Default: today's events
    elif event_type == "total":
        events = Event.objects.all()
    elif event_type == "upcoming":
        events = Event.objects.filter(date__gte=today)
    elif event_type == "past":
        events = Event.objects.filter(date__lt=today)
    else:
        events = Event.objects.none()

    context = {
        "total_participants": total_participants,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "events": events,
        "selected_type": event_type,
        "participants": participants
    }
    return render(request, 'organizer.html', context)

def event_detail(request,id):
    event = Event.objects.prefetch_related('enrld').get(id=id)
    context = {
        "event":event
    }
    return render(request, 'event_detail.html', context)
def add_event(request):
    event_form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            return redirect('home_view')
    context = {"event_form": event_form}
    return render(request, "add_event.html", context)

def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('organizer-dashboard')
    else:
        event_form = EventModelForm(instance=event)
    context = {"event_form": event_form}
    return render(request, "update_event.html", context)

def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        return redirect('organizer-dashboard')
    return render(request, "delete_event.html", {"event": event})

def add_category(request):
    category_form = CategoryModelForm()
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('home_view')
    context = {"category_form": category_form}
    return render(request, "add_category.html", context)

def add_participant(request):
    participant_form = ParticipantModelForm()
    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            return redirect('home_view')
    context = {"participant_form": participant_form}
    return render(request, "add_participant.html", context)