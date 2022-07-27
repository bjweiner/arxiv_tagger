#!/usr/bin/env python
#
""" read from the arxiv search API or RSS feed
read a list of tag names from a text file
and create a webpage that allows you to tag preprints with
javascript buttons or similar, and write the tagging data to a text file

Requires feedparser - pip install feedparser

arxiv_fortune_cookie is a simplified version of arxiv_tagger that
has the tagging/javascript commented out, but adds a suffix like
"in the era of JWST" to each paper title

BJW, May 9 2017  """

import sys
import feedparser
# import commands
import subprocess
import re
import webbrowser

def read_tags(tagfile) :
    tagnames = []
    f = open(tagfile, 'r')
    l = f.readline()
    #    while len(l) <=1 or l[0] =='#' :
    #        l = f.readline()
    while len(l) > 0 :
        if l[0] != '#' and len(l)>1 :
            # Don't split so you can have tags that include a space?
            # Or do split because the output file of tags will be space delimited?
             fields = l.split()
             for tag in fields:
                 tagnames.append(tag)
             #             tagnames.append(l)
        l = f.readline()
    f.close()
    print('Read tag names')
    print(tagnames)
    return tagnames

# This returns a dictionary.  feed.entries has the info for each paper
def read_feed(feedurl) :
    feed = feedparser.parse(feedurl)
    num = len(feed.entries)
    print('Read a feed with', num, ' entries')
    return feed

# create a webpage showing the feed and with javascript or something
# to allow ticking boxes
def create_page(feed, tagnames, pagefile, taggedfile) :
    f = open(pagefile,'w')
    write_header(taggedfile, f)
    # write_jscript_header(taggedfile, f)
    write_entries(feed, tagnames, taggedfile, f)
    write_footer(f)
    f.close()
    return

# basic html header
def write_header(taggedfile, outf) :
    outf.write('<html>')
    outf.write('<head>')
    #outf.write('<title> Astrophysics feed tagger </title>')
    outf.write('<title> Astrophysics feed </title>')
    outf.write('</head>\n')
    # write_jscript_header(taggedfile, outf)
    outf.write('<body>')
    outf.write('<h2> arXiv Astrophysics </h2>\n')
    # outf.write('<form>\n')
    # write_js_textarea(outf)
    return

# html footer 
def write_footer(outf) :
    # outf.write('</form>')
    outf.write('</body>')
    outf.write('</html>')
    return

# Contains the javascript function that is executed when you click a button
def write_jscript_header(taggedfile, outf) :
    outf.write('<script language="JavaScript">\n')
    # outf.write('<!-- Hide script from non-JS browsers\n')
    outf.write('function add_tag(form) {\n')
    outf.write('  var pid = form.id.value\n')
    outf.write('  var tag = form.tag.value\n')
    # Here we need something that writes to a text box. We can't write
    # to a local file from javascript. Might be able to do this with ajax?
    # l = '%s %s \n' % (' form.tags.value ',taggedfile )
    # outf.write(l)
    outf.write('}\n')

    outf.write('function read_tagbox(form) {\n')
    outf.write('  var pid = form.id.value\n')
    outf.write('  var tagbox = form.tagbox.value\n')
    # Here we need something that writes to a text box. We can't write
    # to a local file from javascript. 
    # l = '%s %s \n' % (' write something to ',taggedfile )
    # outf.write(l)
    outf.write('}\n')

    # return a string of id and tags from the box
    outf.write('function return_tagbox(str) {\n')
    outf.write('  foo = document.getElementById(str) ;\n')
    # outf.write('  idtagstring = this.id + ' ' + this.value ;\n')
    # outf.write('  idtagstring = this.id + ' ' + val ;\n')
    # outf.write('  alert("You clicked id " + str) ;\n')
    outf.write('  idstring = foo.id ;\n')
    outf.write('  valstring = foo.value ; \n')
    outf.write('  idtagstring = idstring + " " + valstring ;\n')
    # outf.write('  alert(idtagstring) ;\n')
    outf.write('  return(idtagstring) ;\n')
    outf.write('}\n')

    # Append id and tags to the textarea
    outf.write('function writetextarea(form, str) {\n')
    outf.write('  old = form.myarea.value ;\n')
    outf.write('  if (old==\'\') {form.myarea.value = str} else {form.myarea.value = old + "\\n" + str} ;\n')
    outf.write('}\n')

    # Read from tagbox and append
    outf.write('function readandwrite(form, idstr) {\n')
    outf.write('  tagstr = return_tagbox(idstr) ;\n')
    outf.write('  writetextarea(form, tagstr) ;\n')
    outf.write('}\n')
    # outf.write(' end hide -->\n')
    outf.write('</script><p>\n')

    return

# make the box where ids + tags will be written
def write_js_textarea(outf) :
    #outf.write('<form action="">\n')
    #outf.write('<textarea style="width:60%" name="myarea" cols="60" rows="10"></textarea> <p>\n')
    outf.write('<textarea style="font-size:10pt" name="myarea" cols="60" rows="12"></textarea> <p>\n')
    #outf.write('</form>\n')
    return

def write_entries(feed, tagnames, taggedfile, outf) :
    # trimfeed = feed
    # Here would like to trim the feed to new listings only
    trimfeed = trim_entries(feed)
    # Limit number for testing
    maxnum = 120
    for p in trimfeed.entries[0:maxnum] :
        write_one_entry(p, tagnames, taggedfile, outf)
    return

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
    print('Trimmed to ',len(trimfeed.entries),' new astro-ph entries')
    return trimfeed

# Print html entry for one paper
def write_one_entry(p, tagnames, taggedfile, outf) :
    l = '%s %s %s %s %s\n' % ('<a href="',p.link,'">',p.id,'</a>')
    outf.write(l)
    # p.title is like 'Title of My Paper. (arXiv:1705.03010v1 [astro-ph.SR])'
    fulltitlestr = p.title
    matchex = r' \(arXiv:.*$'
    titlestr = re.sub(matchex,'',fulltitlestr)
    # This should always match, but test anyway
    test_search = re.search(matchex,fulltitlestr)
    if test_search:
        arxiv_idstr = test_search.group(0)
    else:
        arxiv_idstr = 'Unparsed arXiv ID string'
    # get rid of the trailing period in titlestr
    titlestr = re.sub(r'\.$','',titlestr)
    # Here is where we can append fortune cookie suffixes, but we need to run through
    # a function that deals with a title that ends with punctuation 
    newtitle = title_append(titlestr,"in the era of JWST")
    outf.write('<h3>')
    # For the goofy appended title
    outf.write(newtitle)
    # outf.write(titlestr)
    # outf.write(p.title)
    outf.write('</h3>\n')
    outf.write('<h4>')
    outf.write(arxiv_idstr)
    outf.write('</h4><p>\n')
    l = '%s %s\n' % (p.author_detail.name,'<p>')
    outf.write(l)
    # Here we put the javascript
    # write_jscript_entry(p.id, tagnames, taggedfile, outf)
    outf.write(p.summary)
    outf.write('<p><br><p>\n')
    return

# Append some suffix to a title, but if the title ends with punctuation,
# put the suffix before the punctuation
def title_append(titlestr,suffix):
    end_punct_regex = r'[\.\?\!;,]+$'
    test_match = re.search(end_punct_regex,titlestr)
    if test_match:
        end_punct = test_match.group(0)
    else:
        end_punct = ''
    mainstr = re.sub(end_punct_regex,'',titlestr)
    newstr = mainstr + ' ' + suffix + end_punct
    return newstr

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
    # outlist1 = list_jscript_entry(p.id)
    outlist = outlist + outlist1
    outlist.append(p.summary)
    outlist.append('<p><br><p>\n')
    return outlist

# This writes the javascript - have a series of buttons with tagnames,
# or a text entry box where you type tagnames, and an action that
# prints them to taggedfile
def write_jscript_entry(paperid, tagnames, taggedfile, outf) :
    # write_jscript_entry_buttons(paperid, tagnames, taggedfile, outf)
    write_jscript_entry_textbox(paperid, tagnames, taggedfile, outf)
    return

def list_jscript_entry(paperid) :
    # list_jscript_entry_buttons(paperid, tagnames, taggedfile, outf)
    outlist = list_jscript_entry_textbox(paperid)
    return outlist

# Try to have a series of buttons one for each pre defined tag    
def write_jscript_entry_buttons(paperid, tagnames, taggedfile, outf) :
    outf.write('<form>')
    # a little bogus to put the id in a box but it allows passing in the value of paper id
    l = '%s %s %s\n' % ( '<input type="text" name="id" size="24" value="',paperid,'">')
    outf.write(l)
    for t in tagnames :
        # Not sure this is going to work since more than one button will be named "tag"
        l = '%s %s %s\n' % ('<input type="button" name="tag" value="',t,'" onclick=add_tag(this.form)">')
        outf.write(l)
    outf.write('</form> <p>')
    return

# Just have a box where you type the tags you want
def write_jscript_entry_textbox_form_old(paperid, tagnames, taggedfile, outf) :
    outf.write('<form>')
    # a little bogus to put the id in a box but it allows passing in the value of paper id
    l = '%s %s %s\n' % ( '<input type="text" name="id" size="24" value="',paperid,'">')
    outf.write(l)
    l = '%s %s %s\n' % ('<input type="text" name="tagbox" size="50" value="','','" onclick=read_tagbox(this.form)">')
    outf.write(l)
    outf.write('</form> <p>')
    return

# Just have a box where you type the tags you want and an enter button
def write_jscript_entry_textbox(paperid, tagnames, taggedfile, outf) :
    #outf.write('<form name="' + paperid + '" action="">')
    # How to pass in id?
    l = '%s%s%s%s\n' % ( paperid,' <input type="text" name="tagbox" size="50" value=""  id="',paperid,'">')
    outf.write(l)
    # l = '%s%s%s\n' % ('<input type="button" name="tagbutton" value="enter tags" onClick="return_tagbox(\'',paperid,'\')">')
    l = '%s%s%s\n' % ('<input type="button" name="tagbutton" value="enter tags" onClick="readandwrite(this.form,\'',paperid,'\')">')
    outf.write(l)
    #outf.write('</form> <p>')
    return

def list_jscript_entry_textbox(paperid) :
    #outf.write('<form name="' + paperid + '" action="">')
    # How to pass in id?
    outlist = []
    l = '%s%s%s%s\n' % ( paperid,' <input type="text" name="tagbox" size="50" value=""  id="',paperid,'">')
    outlist.append(l)
    # l = '%s%s%s\n' % ('<input type="button" name="tagbutton" value="enter tags" onClick="return_tagbox(\'',paperid,'\')">')
    l = '%s%s%s\n' % ('<input type="button" name="tagbutton" value="enter tags" onClick="readandwrite(this.form,\'',paperid,'\')">')
    outlist.append(l)
    #outf.write('</form> <p>')
    return outlist

def spawn_browser(pagename, taggedfile) :
    # Here we would initiate a browser pointing at the local file given by pagename
    # print 'Point your browser to ', pagename, ' until this can be auto-started'
    # browserloc = '/Applications/Google\ Chrome.app'
    # browserloc = ''
    # cmd = 'open ' + browserloc + ' ' + pagename
    if sys.platform == 'darwin':
        subprocess.Popen(['open', pagename])
    else:
        try:
            webbrowser.open(pagename, new=2)
        except:
            print("Please open a browser on ",pagename)
    # (status, output) = commands.getstatusoutput(cmd)
    # if status :
    #    sys.stderr.write(output)
    #    print("Please open a browser on ",pagename)
    #    sys.exit(1)
    # prompt for text input to pause until the output file is written
    # foo = raw_input('Hit return to continue once you finish tagging: ')
    return

def make_tagged_dict(taggedfile) :
    # read the file of tagged entries and make a dictionary
    # format of file could be paper-ID and list of tags on one line
    # or paper-ID and one tag per line, a paper-ID can occur more than once
    tagdict = {}
    f = open(taggedfile,'r')
    l = f.readline()
    while len(l) > 0 :
        if len(l) > 1 :
            fields = l.split()
            # assume one tag per line.
            paperid = fields[0]
            tag = fields[1]
            if paperid in tagdict: tagdict[paperid].append(tag)
            else: tagdict[paperid] = tag
        l = f.readline()
    f.close()
    return tagdict

def print_tagged(tagdict) :
    pids = sorted(tagdict.keys())
    for p in pids: 
        print(p, tagdict[p])
    return
    
def main() :
    tagfile = 'arxiv_tagnames.txt'
    taggedfile = 'arxiv_tagged.txt'
    # old location
    # feedurl = 'http://arxiv.org/rss/astro-ph'
    feedurl = 'http://export.arxiv.org/rss/astro-ph'
    # for testing, uncomment these lines to use a local file`
    # localfeedurl = 'file:///Users/bjw/programs/arxiv_parser/astro-ph.rss.2014jan03'
    # feedurl = localfeedurl
    pagename = 'arxiv_tagging.html'
    
    if len(sys.argv) == 3 :
        tagfile = sys.argv[1]
        outfile = sys.argv[2]

    # tags = read_tags(tagfile)
    tags = ''
    apfeed = read_feed(feedurl)
    create_page(apfeed, tags, pagename, taggedfile)
    spawn_browser(pagename, taggedfile)

    # currently there's no output file so make_tagged_dict doesn't read anything
    # tagdict = make_tagged_dict(taggedfile)
    # print_tagged(tagdict)


if __name__ == '__main__':
    main()

