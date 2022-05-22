#Swarmimgwithpython.py
#Version : b13(2022-02-19)
#Made By MellDa(MellDa#0001)
#Do not reupload without permission.
import socket
from bs4 import BeautifulSoup
import requests
import sys
import time
def getbyte(string_):
    temp=len(string_.encode('utf-8'))
    temp2 = bytes(chr(temp), encoding='utf-8')
    if len(temp2) > 1:
        return b"\x00"+bytes(chr(temp), encoding='utf-8')[1:]
    else:
        return b"\x00"+bytes(chr(temp), encoding='utf-8')
def returntobyte(string_):
    string_="swarm exec {0} ".format(prefix)+string_
    Textfin=getbyte(string_)+string_.encode('utf-8')
    return Textfin
def prefilterlist(fname):
    f = open(fname, 'r', encoding='UTF8')
    filterlist=[]
    lines = f.readlines()
    for line in lines:
        filterlist.append(line.strip("\n"))
    f.close()
    return filterlist


#Setting Server
host="127.0.0.1"
port=420

#Setting DC
dcid="steve"
mgall=True
lastpostid=152750
isrecommend=False
filterlist=prefilterlist("Filter_ko_KR.txt")
request_headers = { 
'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
Safari/537.36'), }
page=1
firstcycle=True

#Setting Chat
prefix="> [DtC]"
timedelay=[10,10,20,50]

if mgall:
    connectmessage="Connected to Gallery : {0}(Minor) / Made by MellDa".format(dcid)
    crawlargs=[4,-5,-4,2]
else:
    connectmessage="Connected to Gallery : {0} / Made by MellDa".format(dcid)
    crawlargs=[3,-5,-4,1]

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(2)
conn, addr = s.accept()
print(addr, "Now Connected")

#Welcome Message
conn.send(returntobyte(connectmessage))
time.sleep(timedelay[0])
if isrecommend:
    connectmessage="It will now send a new recommended post."
else:
    connectmessage="It will now send a new post."
conn.send(returntobyte(connectmessage))
time.sleep(timedelay[1])

#Crawling
while True:
    print("Finding...")
    newpost=[]
    isfull=True
    while isfull:
        if mgall:
            if isrecommend:
                url = 'https://gall.dcinside.com/mgallery/board/lists?id={0}&page={1}&exception_mode=recommend'.format(dcid,page)
            else:
                url = 'https://gall.dcinside.com/mgallery/board/lists?id={0}&page={1}'.format(dcid,page)
        else:
            if isrecommend:
                url = 'https://gall.dcinside.com/board/lists?id={0}&page={1}&exception_mode=recommend'.format(dcid,page)
            else:
                url = 'https://gall.dcinside.com/board/lists?id={0}&page={1}'.format(dcid,page)
        response = requests.get(url,headers=request_headers)
        if response.status_code == 200:
            html = response.text
            if not html:
                conn.send(returntobyte("Disconnected with DC Server, Quitting..."))
            soup = BeautifulSoup(html, 'html.parser')
        else:
            conn.send(returntobyte("Disconnected with DC Server, Quitting..."))
            sys.exit()
        a=soup.find_all("tr",{'class':'ub-content us-post'})
        page += 1
        for i in a:
            temp=i.get_text().split("\n")
            if temp[crawlargs[3]] != "공지":
                if int(temp[1]) > lastpostid:
                    newpost.append(temp)
                    if len(newpost) == 10:
                        break
                else:
                    isfull=False
                    if not isrecommend:
                        break
    page=1
    if newpost:
        lastpostid=int(newpost[0][1])
        if not firstcycle:
            newpost.reverse()
            print("Done, Founded : {0}".format(len(newpost)))
            if len(newpost) == 10:
                conn.send(returntobyte("Found new post. / Count : {0}(Max), Uploading...".format(len(newpost))))
            else:
                conn.send(returntobyte("Found new post. / Count : {0}, Uploading...".format(len(newpost))))
            time.sleep(timedelay[1])
            for i in newpost:
                Textmain=i[crawlargs[0]]+" / "+i[crawlargs[1]]+"/ "+i[crawlargs[2]]
                for j in filterlist:
                    if Textmain.find(j) != -1:
                        Textmain=Textmain.replace(j, "*"*len(j))
                    else:
                        if len(j)==2:
                            if Textmain.find((j[0]+"@"+j[1])) != -1:
                                Textmain=Textmain.replace(j, "*@*")
                conn.send(returntobyte(Textmain))
                time.sleep(timedelay[2])
            time.sleep(timedelay[3]-min(timedelay[3]-1,timedelay[2]*len(newpost)))
        else:
            print("Updated")
            firstcycle=False
            time.sleep(timedelay[2])
    else:
        print("Done, Nothing Founded")
        time.sleep(timedelay[3])