import json
from functools import wraps
from flask import session,redirect,url_for
import itertools

def from_log(folder,start,end):
    if start < 0 or (end != 'end' and end < 0):
        raise ValueError
    with open(folder+'/log.json') as f:
        names = json.load(f)['names']
        collection = '{"data":[%s],"error":false}'
        items = []
        for n in names[start:(len(names) if end=='end' else end)]:
            with open(folder+'/'+n) as e:
                items.append(e.read())
        return collection % ','.join(items)

def update_log(folder,fileName):
    with open(folder+'/log.json') as f:
        names = json.load(f)['names']
        json.dump({'names':[fileName]+names},open(folder+'/log.json','w'))

def next_element(lang,folder):
    with open('data/'+lang+'/'+folder+'/log.json') as f:
        names = json.load(f)['names']
        if len(names)==0:
            return 'item0.json'
        fName=names[0][:-5]
        value = ''.join(itertools.takewhile(lambda x:x.isdigit(),reversed(fName)))[::-1]
        nName = fName[:-len(value)]+str(int(value)+1)
        return nName+'.json'

def del_log(folder,index):
    with open(folder+'/log.json') as f:
        names = json.load(f)['names']
        del names[index]
        json.dump({'names':names},open(folder+'/log.json','w'))

def update_element_using_index(folder,index, contents):
    with open(folder+'/log.json') as f:
        name = json.load(f)['names'][index]
        jsondata = json.load(open(folder+'/'+name))
        jsondata.update(contents)
        json.dump(jsondata, open(folder+'/'+name,"w"))

def sessionvalidated(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if "loggedIn" not in session:
            return redirect(url_for("ui.login"))
        elif session["loggedIn"] == False:
            return redirect(url_for("ui.login"))
        else:
            return f(*args,**kwargs)
    return wrapper

def formattime(current):
    if current.hour % 12 == 0:
        hour = 12
    else:
        hour = current.hour % 12
    if current.minute >= 10:
        minute = current.minute
    else:
        minute = "0"+current.minute
    if current.hour >= 12:
        sig = "PM"
    else:
        sig = "AM"
    return "{}:{} {}".format(hour,minute,sig)
