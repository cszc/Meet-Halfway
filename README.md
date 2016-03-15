Meet Halfway
============

We are using an environment manager (conda) to manage the requirements
for this project.

Please run "source activate pllc" prior to running any of our code to
activate the environment

About
-----

Given two starting locations, preferred modes of transit, and a desired type of location (coffee shop, restaurant, bar, etc.), Meet Halfway finds a meeting destination with roughly equal travel times for both parties. Meet Halfway currently works for addresses within the United States.

Meet Halfway is a Django app that uses SQLite3 for the database, and Bootstrap for the front end.

Dependencies
------------

-	[BootstrapForms](https://github.com/tzangms/django-bootstrap-form) `pip install django-bootstrap-form`
-	[Django](https://www.djangoproject.com/)
-	[GoogleMaps](https://github.com/googlemaps/)
-	[lxml](http://lxml.de/)
-   [Conda](http://conda.pydata.org/docs/intro.html) (for environment management)
-	[RandomWords](https://pypi.python.org/pypi/RandomWords/0.1.5)
-	[Requests](http://docs.python-requests.org/en/master/)
-	[PYUSPS](https://github.com/pmack1/pyusps)
	-	note this has been modified to work with Python 3
-	Also used:
	-	json
	-	time
	-	re
	-	csv
	-   sqlite3
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

Save the Google Maps key in a text file called "apikeys.txt" in two places: the top-level directory, and the folder meethalfway

You will also need a key for the [USPS Address Information API](https://www.usps.com/business/web-tools-apis/welcome.htm). Save the USPS key in a text file called "uspskey.txt" in the top-level directory

*Note all necessary API keys have been included in our virtual machine

Banner Image
------------

["Ferris"](https://www.flickr.com/photos/mr-numb/8587170664/in/photolist-e5PuEC) by Adam Simmons is licensed under CC BY-NC-ND 2.0
