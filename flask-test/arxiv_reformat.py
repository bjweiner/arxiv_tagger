
import sys
import feedparser
import commands
import re

# This returns a dictionary.  feed.entries has the info for each paper
def read_feed(feedurl) :
    feed = feedparser.parse(feedurl)
    num = len(feed.entries)
    print 'Read a feed with', num, ' entries'
    return feed

def list_entries(feed) :
    # trimfeed = feed
    # Here would like to trim the feed to new listings only
    trimfeed = trim_entries(feed)
    # Limit number for testing
    maxnum = 120
    outlist = []
    for p in trimfeed.entries[0:maxnum] :
        outlist1 = list_one_entry(p)
        #outlist.append(outlist1)
        outlist = outlist + outlist1
        outlist.append('\n')
    return outlist

# Trim out cross-lists and revisions by searching the title_detail string:
# must find 'astro-ph', must not end with 'UPDATED)'
# Copy all the feed properties and just trim the entries list. This seems to work.
def trim_entries(feed) :
    trimfeed = feed
    trimmed_entries = []
    for p in feed.entries :
        match1 = re.search('astro-ph',p.title_detail.value)
        match2 = re.search(r'UPDATED\)$',p.title_detail.value)
        if (match1 and not match2) : trimmed_entries.append(p)
    trimfeed.entries = trimmed_entries
    print 'Trimmed to ',len(trimfeed.entries),' new astro-ph entries'
    return trimfeed

def list_one_entry(p) :
    outlist = []
    l = '%s %s %s %s %s\n' % ('<a href="',p.link,'">',p.id,'</a>')
    outlist.append(l)
    outlist.append('<h3>')
    outlist.append(p.title)
    outlist.append('</h3><p>\n')
    l = '%s %s\n' % (p.author_detail.name,'<p>')
    outlist.append(l)
    # Here we put the javascript
    outlist1 = list_jscript_entry(p.id)
    outlist = outlist + outlist1
    outlist.append(p.summary)
    outlist.append('<p><br><p>\n')
    return outlist

def list_jscript_entry(paperid) :
    # list_jscript_entry_buttons(paperid, tagnames, taggedfile, outf)
    outlist = list_jscript_entry_textbox(paperid)
    return outlist

def list_jscript_entry_textbox(paperid) :
    #outf.write('<form name="' + paperid + '" action="">')
    # How to pass in id?
    outlist = []
    l = '%s%s%s%s\n' % ( paperid,' <input type="text" style="font-size:12pt" name="tagbox" size="50" value=""  id="',paperid,'">')
    outlist.append(l)
    # l = '%s%s%s\n' % ('<input type="button" name="tagbutton" value="enter tags" onClick="return_tagbox(\'',paperid,'\')">')
    l = '%s%s%s\n' % ('<input type="button" style="font-size:12pt" name="tagbutton" value="enter tags" onClick="readandwrite(this.form,\'',paperid,'\')">')
    outlist.append(l)
    #outf.write('</form> <p>')
    return outlist

