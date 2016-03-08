from django.shortcuts import render, redirect
#import googlemaps
import csv
import time
import json
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from . import models



class EnterIDForm(forms.Form):
    trip_id = forms.CharField()
    def validate_trip_id(self):
        cleaned_id = self.cleaned_data
        if models.Meeting.objects.filter(trip_id = cleaned_id['trip_id']):
            return cleaned_id['trip_id']
        else:
            return None

class AddAddress(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = ["street", "city", "state", "zip_code"]


class AddParticipant(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ["transit_mode"]
        widgets = {
            'transit_mode': forms.Select(),
        }


class AddMeeting(forms.ModelForm):
    class Meta:
        model = models.Meeting
        fields = ["business_type", "share_location"]
        widgets = {
            'business_type': forms.Select(),
            'share_location': forms.CheckboxInput()
        }

def home(request):
    error = None
    if request.method == 'POST':
        if "participant_one_submit" in request.POST:
            address = AddAddress(request.POST)
            participant = AddParticipant(request.POST)
            meeting = AddMeeting(request.POST)
            if address.is_valid() and participant.is_valid() and meeting.is_valid():
                trip_id = participant_one(request, address, participant, meeting)
                return redirect('meethalfway:new_meeting', trip_id)
        elif 'enter_trip_id' in request.POST:
            trip_id = EnterIDForm(request.POST)
            if trip_id.is_valid():
                valid_trip_id = trip_id.validate_trip_id()
                if valid_trip_id:
                    meeting = models.Meeting.objects.get(trip_id = valid_trip_id)
                    if not meeting.participant_two:
                        return redirect('meethalfway:participant_two', valid_trip_id)
                    else:
                        return redirect('meethalfway:results', valid_trip_id)
                else:
                    error = True

    address = AddAddress()
    participant = AddParticipant()
    meeting = AddMeeting()
    trip_id = EnterIDForm()


    c = {
        'forms': [address, participant, meeting],
        'trip_id_form': trip_id,
        'not_found' : error
    }

    return render(request, 'halfwayapp/home.html', c)

def new_meeting(request, trip_id):
    return render(request,'halfwayapp/response.html', {'uniq' : trip_id})

def participant_one(request, address, participant, meeting):
    address_obj = address.save()
    part_obj = participant.save()
    part_obj.starting_location = address_obj
    part_obj.save()
    meeting_obj = meeting.save()
    meeting_obj.participant_one = part_obj
    meeting_obj.trip_id = meeting_obj.random_words()
    meeting_obj.save()

    return meeting_obj.trip_id

def participant_two(request, trip_id):
    if request.method == 'POST':
        address = AddAddress(request.POST)
        participant = AddParticipant(request.POST)
        if address.is_valid() and participant.is_valid():
            address_obj = address.save()
            part_obj = participant.save()
            part_obj.starting_location = address_obj
            part_obj.save()
            meeting = models.Meeting.objects.get(trip_id = trip_id)
            meeting.participant_two = part_obj
            meeting.save()
            meeting.get_destinations()
            return redirect('meethalfway:results', meeting.trip_id)
    address = AddAddress()
    participant = AddParticipant()

    c = {
        'forms': [address, participant],
        'uniq': trip_id
    }

    return render(request, "halfwayapp/person2.html", c)

def results(request, trip_id):
    meeting = models.Meeting.objects.get(trip_id = trip_id)
    # destinations = meeting.destinations.all()
    d = meeting.destinations.order_by('score')
    destinations = d.reverse()
    best_dest = destinations[:1].get().latlng
    lat = best_dest.split(",")[0]
    lng = best_dest.split(",")[1]
    print("These are the best destination lat lngs ", lat, lng)
    c = {
        'destinations': destinations,
        'trip_id': trip_id,
        'lat': lat,
        'lng': lng
    }
    return render(request, "halfwayapp/results.html", c)

def about(request):
    return render(request, "halfwayapp/about.html")

def contact(request):
    return render(request, "halfwayapp/contact.html")
