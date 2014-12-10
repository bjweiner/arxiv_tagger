
from flask import Flask, render_template
from flask import request, redirect
import sys

import arxiv_reformat as arxtag

print 'Point browser to http://localhost:5000/arxiv_tag'

app = Flask(__name__)

@app.route('/arxiv_tag')
def tagging() :
    #print 'Point browser to http://localhost:5000/arxiv_tag'
    feedurl = 'http://arxiv.org/rss/astro-ph'
    #pagename = 'test_out.html'
    apfeed = arxtag.read_feed(feedurl)
    #tags = ''
    #taggedfile = 'test_tagged.txt'

    #create_page(apfeed, tags, pagename, taggedfile)
    #f = open(pagename,'r')
    #pagestr = f.read()
    outlist = []
    outlist = arxtag.list_entries(apfeed)
    #outlist = arxtag.list_one_entry(apfeed.entries[0])
    #print outlist
    outstr = ''.join(outlist)
    mytitle='arXiv Astrophysics feed tagging'
    myheading='arXiv Astrophysics tagging'
    pagestr = render_template('full_template.html', mytitle=mytitle, myheading=myheading, mainbody=outstr)
    # print outstr
    # pagestr = outstr
    return pagestr

@app.route('/tags', methods=['POST'])
def tags():
    tags = request.form['myarea']
    outstring = "Your papers and tags are:\n" + tags
    print(outstring)
    mytitle = 'arXiv tags'
    myheading = 'arXiv tag output'
    pagestr = render_template('tag_template.html', mytitle=mytitle, myheading=myheading, tagbody=outstring)
    #return redirect('/testing')
    return pagestr
    
#def hello_world():
#    return 'Hello World!'

# def main() :
#    app = Flask(__name__)
#    app.run()

if __name__ == '__main__':
    app.run()
    #testing_fn()
    

