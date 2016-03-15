# Meet Halfway

## About

Given two starting locations, preferred modes of transit, and a desired type of location (coffee shop, restaurant, bar, etc.), Meet Halfway finds a meeting destination with roughly equal travel times for both parties. Meet Halfway currently works for addresses within the United States.

Meet Halfway is a Django app that uses SQLite3 for the database, and Bootstrap for the front end.

## Dependencies
- [GoogleMaps](https://github.com/googlemaps/)
- [Django](https://www.djangoproject.com/)
- [BootstrapForms](https://github.com/tzangms/django-bootstrap-form) `pip install django-bootstrap-form`
- [RandomWords](https://pypi.python.org/pypi/RandomWords/0.1.5)
- [lxml](http://lxml.de/)
- [Requests](http://docs.python-requests.org/en/master/)

## API keys 

You need to have a [Google Maps API](https://developers.google.com/maps/) key enabled for:
- Google Directions
- Google Matrix
- Google Places

Save the Google Maps key in a text file called "apikeys.txt" in two places: the top-level directory, and the folder meethalfway

You will also need a key for the [USPS Address Information API](https://www.usps.com/business/web-tools-apis/welcome.htm). Save the USPS key in a text file called "uspskey.txt" in the top-level directory
