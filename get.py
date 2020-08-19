import os
from flask import Blueprint, send_file, make_response, request
import json
from helper import from_log

get_info = Blueprint('get_info', __name__, url_prefix='/api')

def from_json(name):
    def ret(lang):
        if(os.path.isdir('data/'+lang)):
            return send_file('data/'+lang+'/'+name+'.json')
        else:
            return send_file('data/error.json')
    ret.__name__=name
    get_info.route('<lang>/'+name)(ret)

def numbered_json(name):
    def ret(lang):
        start = int(request.args.get('start', 0))
        end = request.args.get('end','end')
        if end != 'end':
            end = int(end)
        if(os.path.isdir('data/'+lang)):
            r = make_response(from_log('data/'+lang+'/'+name, start, end))
            r.mimetype='application/json'
            return r
        else:
            return send_file('data/error.json')
    ret.__name__=name
    get_info.route('<lang>/'+name)(ret)

from_json('clubs')
from_json('student')
numbered_json('new')
numbered_json('announcements')
numbered_json('events')
numbered_json('teachers')
from_json('modal')
from_json('challenge')
from_json('lunchEvents')
from_json('resources')
from_json('jobObs')
from_json('sslOps')
