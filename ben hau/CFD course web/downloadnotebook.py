'''
downloadnotebook.py
-------------------
Downloads a HTML copy of a nbviewer (http://nbviewer.ipython.org) ipython notebook and replaces the boilerplate.

Requires: BeautifulSoup
'''

import urllib2                  # downloader
from bs4 import BeautifulSoup   # parser
from urlparse import urlparse   # parses url
import re

address = 'http://nbviewer.ipython.org/github/cdohl/PAP751/blob/master/Finite%20Difference%20Techniques/06_velocity%20pressure%20formulation.ipynb'
o = urlparse(address)
filename = o.path.rsplit('/',1)[-1] # All the stuff after the last slash
filename_noext = filename[:-6]      # strip out file extension
page = urllib2.urlopen(address)
html = page.read()
print 'Downloaded page'

soup = BeautifulSoup(html, 'html.parser')

# Everything should be in <div class='notebook'> 
mainbody = soup.find(id='notebook')
print 'Stripped boilerplate'

'''
Output
'''

# The header of our output html file
# Contains the customisation
header = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><!-- Google font --><link href="https://fonts.googleapis.com/css?family=Merriweather:400,700,400italic" rel="stylesheet" type="text/css">'
mathjax = r"<script type=""text/x-mathjax-config"">MathJax.Hub.Config({tex2jax: {inlineMath: [['\$','\$'], ['\\\\(','\\\\)']]}});</script><script type=""text/javascript"" src=""https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML""></script>"
title = '<title>PyCFD: a Pythonic introduction to computational fluid dynamics</title><link href="./css/notebook.css" rel="stylesheet"><link href="../../assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"><!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries --><!--[if lt IE 9]><script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script><script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><![endif]--></head>'
navigation = '<nav class="navbar navbar-inverse navbar-fixed-top"><div class="container"><div class="navbar-header"><button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar"><span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><a class="navbar-brand" href="index.html">PyCFD</a></div><div id="navbar" class="collapse navbar-collapse"><ul class="nav navbar-nav"></ul><ul class="nav navbar-nav navbar-right"><li><a href="' + address + ' ">Download notebook</a></li></ul></div><!--/.nav-collapse --></div></nav>'
footer = '</body></html>'

full_document = header + mathjax + title+ navigation + mainbody.encode('utf-8') + footer
hot_soup = BeautifulSoup(full_document, 'html.parser')
output_code = hot_soup.prettify() # format the code nicely

f = open(filename_noext + '.html', "w")
f.write(output_code.encode('utf-8'))
f.close()
print 'File written, done'
