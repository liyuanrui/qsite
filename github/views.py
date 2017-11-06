from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import re
import os
import requests
from bs4 import BeautifulSoup

def download(request):
    filename=request.GET.get('filename')
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)

    return response
    

def qpython(request):
    urls=['https://github.com/qpython-android/qpython/releases','https://github.com/qpython-android/qpython3/releases']
    msg=[]
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        body = soup.find_all('div',class_='release-body commit open')[0]
        release_title=body.div.a.text
        relative_time=' '.join(body.div.p.text.split()[:6])
        mt=body.find_all('div',class_='markdown-body')[0]
        download='https://github.com'+body.find_all('a',rel='nofollow')[0]['href']
        if 'qpython3' in url:
            m = 'QPython3: <b>%s</b><br /><b>%s</b><br />Download: <a href="%s">releases-qpython3.apk</a>'%(release_title,relative_time,download)
        else:
            m = 'QPython: <b>%s</b><br /><b>%s</b><br />Download: <a href="%s"> releases-qpython.apk</a>'%(release_title,relative_time,download)
        msg.append(m)
    return HttpResponse('<meta name="viewport" content="width=device-width,height=device-height,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"><br /><br />'.join(msg))
