image-extrator
==============

This is a simple web application that is able to extract images from urls and caches them. It's using [Reddit's scraper code](https://github.com/reddit/reddit/blob/master/r2/r2/lib/scraper.py), with a couple small tweaks, mostly to allow it to run on [Google App Engine](https://developers.google.com/appengine/).

The app provides a single call: <code>/?url=<url></code>, which will return a URL corresponding to the location of that image. Your app should cache that url.
Please note that the URL returned may also be a redirect url, which should 'soon' redirect to the actual image when it's been extracted.

Deploy
------

1. Signup or log in to [Google App Engine](https://developers.google.com/appengine/)
2. Create a new application, name it in a non-guessable way if you want to be the only one using it :)
3. Checkout the code : `git clone git://github.com/superfeedr/image-extrator.git`
4. Update your application name’s in app.yaml, line 1 (replace `image-extrator`) with whatever you chose at step 2.
5. Deploy your instance.

You will quickly (100,000 requests/day) bump into Google App Engine's limit for the 1GB incoming bandwidth. Upgrade to a "paid" app... but don't worry too much, as the [incoming bandwidth is free](http://cloud.google.com/pricing/) on Google App Engine! 

Enjoy!