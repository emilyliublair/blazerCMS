import json
from functools import wraps
from flask import session,redirect,url_for

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
