# arxiv_tagger
Code for parsing the astro-ph arxiv feed and adding tags to articles

The arxiv_tagger codereads the arXiv astro-ph rss feed and reparses it into a web page that
uses some javascript to allow you to type in keywords for any abstracts you are interested in.
The abstract ID/url and the keywords appear in a text box at the top of the page. The intent
of this was to export the keywords to some external database, so that you could read astro-ph
every day and tag articles you wanted to remember into various subject headings, like an 
ADS private library. Javascript security restrictions mean that the tags have to be displayed
rather than exported to a local file (i.e. javascript can't simply write to some file on your 
disk).  The long term future of making this work would be to run it as some kind of 
lightweight web service e.g. using Flask. Unfortunately, there doesn't seem to be an API for
the ADS private libraries, so it's difficult to integrate with that.

arxiv_fortune_cookie is a variant that comments out the javascript and simply reads astro-ph 
and redisplays it with a suffix added to each title, currently "in the era of JWST" - thus all
papers will look like "The black hole - bulge mass relation revisited in the era of JWST". It
correctly handles titles that end with punctuation. It is named after the game where everyone
at the table opens their fortune cookies and reads them, adding "in bed" as a suffix.

To run the code, download it and install feedparser:
pip install feedparser
python arxiv_fortune_cookie.py

This should create a local webpage and open a web browser on it.

