import os
from flask import Blueprint, send_file, make_response, request
import json

get_info = Blueprint('get_info', __name__, url_prefix='/api')

@get_info.route('/<lang>/events')
def events(lang):
    start = int(request.args.get('start', 0))
    end = request.args.get('end','end')
    if end != 'end':
        end = int(end)
    if(os.path.isdir('data/'+lang)):
        r = make_response(from_log('data/'+lang+'/events', start, end))
        r.mimetype='application/json'
        return r
    else:
        return send_file('data/error.json')

@get_info.route('/<lang>/announcements')
def announcements(lang):
    start = int(request.args.get('start', 0))
    end = request.args.get('end','end')
    if end != 'end':
        end = int(end)
    if(os.path.isdir('data/'+lang)):
        r = make_response(from_log('data/'+lang+'/announcements', start, end))
        r.mimetype='application/json'
        return r
    else:
        return send_file('data/error.json')
    

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
