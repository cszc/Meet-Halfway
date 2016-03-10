from django.shortcuts import render, redirect
import csv
import time
import json
import requests
from django.core.urlresolvers import reverse
from django import forms
from . import models


class EnterIDForm(forms.Form):
    '''
    Short form to enter in a meeting ID. Validate_trip_id function cleans the
    ID and checks if it is in the database; if it isn't, returns None.
    '''
    trip_id = forms.CharField()
    def validate_trip_id(self):
        cleaned_id = self.cleaned_data
        if models.Meeting.objects.filter(trip_id = cleaned_id['trip_id']):
            return cleaned_id['trip_id']
        else:
            return None


class AddAddress(forms.ModelForm):
    '''
    ModelForm connected to the Address model. Provides field for street, city,
    state, and zip code.
    '''
    class Meta:
        model = models.Address
        fields = ["street", "city", "state", "zip_code"]


class AddParticipant(forms.ModelForm):
    '''
    ModelForm connected to the Paricipant model. Provides a menu of valid modes
    of transport. An address is combined with mode of transit to create a Participant
    '''
    class Meta:
        model = models.Participant
        fields = ["transit_mode"]
        widgets = {
            'transit_mode': forms.Select(),
        }


class AddMeeting(forms.ModelForm):
    '''
    ModelForm connected to the Meeting model. Provides a menu of valid business
    types. Created when a participant is added and initialized with empty values for
    participant_two and destinations.
    '''
    class Meta:
        model = models.Meeting
        fields = ["business_type", "share_location"]
        widgets = {
            'business_type': forms.Select()
        }


def home(request):
    '''
    View for home page of MeetHalfway. Contains forms for the first participant to
    enter their address, mode of transit, and business type for meeting. Validates
    the address provided using a service from USPS. With completed form, creates an
    Address, Participant, and Meeting then generates a unique Meeting ID. Also
    displays a form to enter in the ID of a previously created meeting. If valid,
    either redirects to a page for the second participant to enter information or
    displays results if second person's information has already been added. If
    invalid, displays error message.
    '''
    error = None
    if request.method == 'POST':
        if "participant_one_submit" in request.POST:
            address = AddAddress(request.POST)
            participant = AddParticipant(request.POST)
            meeting = AddMeeting(request.POST)
            #USPS api used to validate the entered address
            if address.is_valid() and participant.is_valid() and meeting.is_valid():
                trip_id, suggestion = participant_one(request, address, participant, meeting)
                if trip_id != None:
                    return redirect('meethalfway:new_meeting', trip_id)
                else:
                    #Returns error message if address invalid
                    return redirect('meethalfway:address_error1',suggestion)
        elif 'enter_trip_id' in request.POST:
            trip_id = EnterIDForm(request.POST)
            if trip_id.is_valid():
                valid_trip_id = trip_id.validate_trip_id()
                if valid_trip_id:
                    meeting = models.Meeting.objects.get(trip_id = valid_trip_id)
                    if not meeting.participant_two:
                        #Redirects to form for participant two if not filled in
                        return redirect('meethalfway:participant_two', valid_trip_id)
                    else:
                        #Redirects to results if information already filled int
                        return redirect('meethalfway:results', valid_trip_id)
                else:
                    #Error if invalid trip id is entered
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
    '''
    Displays the trip id generated after participant one enters information.
    '''
    return render(request,'halfwayapp/response.html', {'uniq' : trip_id})


def participant_one(request, address, participant, meeting):
    '''
    Function to verify the address of the first participant and to create and save
    the Address, Participant, and Meeting objects for the new meeting.
    '''
    address_obj = address.save()
    verify, suggestion,verified_address_dict = address_obj.verify_address()
    if verify:
        verified_address = models.Address(street = verified_address_dict['address'], city = verified_address_dict['city'], \
        state = verified_address_dict['state'], zip_code = verified_address_dict['zip5'])
        verified_address.save()
        address_obj.delete()

        part_obj = participant.save()
        part_obj.starting_location = verified_address
        part_obj.save()

        meeting_obj = meeting.save()
        meeting_obj.participant_one = part_obj
        meeting_obj.trip_id = meeting_obj.random_words()
        meeting_obj.save()
    else:
        #Returns error message if address invalid
        return None, suggestion

    return meeting_obj.trip_id, None


def participant_two(request, trip_id):
    '''
    Handles information passed to create the second participant in a Meeting. If
    a second participant has already been added, redirects to results. Otherwise,
    creates a participant_two and calls get_destinations function.
    '''
    if request.method == 'POST':
        meeting = models.Meeting.objects.get(trip_id = trip_id)
        if meeting.participant_two:
            #If second participant already added, redirects to results
            return redirect('meethalfway:results', trip_id)
        address = AddAddress(request.POST)
        participant = AddParticipant(request.POST)
        if address == meeting.participant_one.starting_location:
            return redirect('meethalfway:no_results')
        if address.is_valid() and participant.is_valid():
            address_obj = address.save()
            #USPS api used to validate the entered address
            verify, suggestion, verified_address_dict = address_obj.verify_address()
            if verify:
                verified_address = models.Address(street = verified_address_dict['address'], city = verified_address_dict['city'], \
                state = verified_address_dict['state'], zip_code = verified_address_dict['zip5'])
                verified_address.save()
                address_obj.delete()

                part_obj = participant.save()
                part_obj.starting_location = verified_address
                part_obj.save()

                meeting.participant_two = part_obj
                meeting.save()
                meeting.get_destinations()

            else:
                return redirect('meethalfway:address_error2', trip_id, suggestion)
            return redirect('meethalfway:results', trip_id)
    address = AddAddress()
    participant = AddParticipant()

    c = {
        'forms': [address, participant],
        'uniq': trip_id
    }
    return render(request, "halfwayapp/person2.html", c)


def results(request, trip_id):
    '''
    When called, finds the Meeting object associated with the trip id. Shows the
    destination results if any were found and displays error message otherwise.
    '''
    meeting = models.Meeting.objects.get(trip_id = trip_id)
    d = meeting.destinations.order_by('score')
    if not d.exists():
        return redirect('meethalfway:no_results')
    destinations = d.reverse()
    best_dest = destinations[:1].get().latlng
    lat = best_dest.split(",")[0]
    lng = best_dest.split(",")[1]

    c = {
        'destinations': destinations,
        'trip_id': trip_id,
        'lat': lat,
        'lng': lng
    }
    return render(request, "halfwayapp/results.html", c)


def about(request):
    '''
    Displays 'about' page with information about site.
    '''
    return render(request, "halfwayapp/about.html")

def no_results(request):
    return render(request, "halfwayapp/no_results.html")

def contact(request):
    '''
    Displays 'contact' page.
    '''
    return render(request, "halfwayapp/contact.html")


def address_error1(request, suggestion):
    '''
    Displays error message if first participant's address is invalid.
    '''
    c = {
        'suggestion': suggestion
    }
    return render(request, "halfwayapp/address_error1.html", c)


def address_error2(request, trip_id, suggestion):
    '''
    Displays error message if second participant's address is invalid.
    '''
    c = {
        'trip_id': trip_id,
        'suggestion': suggestion
    }
    return render(request, "halfwayapp/address_error2.html", c)
