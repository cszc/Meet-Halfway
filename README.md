Meet Halfway
============

Given two starting locations, preferred modes of transit, and a desired type of location (coffee shop, restaurant, bar, etc.), Meet Halfway finds meeting destinations with roughly equal travel times for both parties.

The platform preserves privacy so that you can meet friends, strangers, or acquaintances without revealing your address.  Suggestions are provided with fairness scores and approximate travel times to help inform your decision. Meet Halfway currently works for addresses within the United States.

Meet Halfway is a Django app that uses PostgreSQL for the database, and Bootstrap for the front end.

Try it out at [www.meethalfway.io](www.meethalfway.io).

Dependencies
------------
Dependencies are listed in requirements.txt.
Install with: `pip install -r requirements.txt` in a new virtual environment, or install separately:

-	[BootstrapForms](https://github.com/tzangms/django-bootstrap-form) `pip install django-bootstrap-form`
-	[Django](https://www.djangoproject.com/)
-	[GoogleMaps](https://github.com/googlemaps/)
-	[lxml](http://lxml.de/)
-   [Conda](http://conda.pydata.org/docs/intro.html) (for environment management)
-	[RandomWords](https://pypi.python.org/pypi/RandomWords/0.1.5)
-	[Requests](http://docs.python-requests.org/en/master/)
-	[PYUSPS](https://github.com/pmack1/pyusps) (used for address validation)
	- note this has been modified to work with Python 3
-   [psycopg2](http://initd.org/psycopg/)
-   [dj-database-url](https://github.com/kennethreitz/dj-database-url) (for accessing database environment variables)
-   [whitenoise](https://pypi.python.org/pypi/whitenoise) (for serving static files)
- [gunicorn](http://gunicorn.org/)
-	Also used:
	-	json
	-	time
	-	re
	-	csv
-	CSS, HTML, and jQuery adapted from:
	-	[clipboard.js](https://clipboardjs.com/)
		-	for copying text to clipboard
	-	[Bootstrap](http://getbootstrap.com/)
		-	framework for responsive html, css, and js
	-	[Loaders.css](https://github.com/ConnorAtherton/loaders.css/tree/master)
		-	CSS loading animation
		-	MIT Licensed Copyright (c) 2016 Connor Atherton

API Keys
--------

You need to have a [Google Maps API](https://developers.google.com/maps/) key enabled for: - Google Directions - Google Distance Matrix - Google Places

You will also need a key for the [USPS Address Information API](https://www.usps.com/business/web-tools-apis/welcome.htm).

Contributors
-----------
Built by four [CAPP](https://capp.sites.uchicago.edu/) students for UChicago's [CS122, Winter 2016](https://www.classes.cs.uchicago.edu/archive/2016/winter/12200-1/).

[Christine Chung](github.com/cszc)
[Lauren Dyson](https://github.com/ldyson)
[Paul Mack](https://github.com/pmack1)
[Leith McIndewar](https://github.com/lmcindewar)

Banner Image
------------

["Ferris"](https://www.flickr.com/photos/mr-numb/8587170664/in/photolist-e5PuEC) by Adam Simmons is licensed under CC BY-NC-ND 2.0
