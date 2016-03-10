"""djangohalfway URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'home', views.home, name='home'),
    url(r'^new_meeting/(?P<trip_id>[a-z]+-[a-z]+-[a-z]+)', views.new_meeting, name = 'new_meeting'),
    url(r'^participant_two/(?P<trip_id>[a-z]+-[a-z]+-[a-z]+)', views.participant_two, name = 'participant_two'),
    url(r'^results/(?P<trip_id>[a-z]+-[a-z]+-[a-z]+)', views.results, name = 'results'),
    url(r'^address_error1/(?P<suggestion>.*)', views.address_error1, name = 'address_error1'),
    url(r'^address_error2/(?P<trip_id>[a-z]+-[a-z]+-[a-z]+)(?P<suggestion>.*)', views.address_error2, name = 'address_error2'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),<<<<<<< HEAD
    url(r'^no_results', views.no_results, name='no_results'),
    url(r'$', views.home, name='home')

]
# urlpatterns += staticfiles_urlpatterns()
