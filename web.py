import model
import config

from gevent import monkey; 
monkey.patch_all()
from bottle import route, run, template, request, abort, redirect, static_file


fileServer = model.FileServer(config.fileStorePath());
soundServer = model.SoundServer();
database = model.Database(config.mongoConnect(), config.mongoDatabaseName());

@route('/view/<skip:int>')
def view(skip):
    rows = [['file', 'attributes', 'transcriptions']]
    limit = 20
    for record in database.getRecords(skip, limit):
        if record.has_key('file'):
            rows.append(
                ['<a href="/soundfiles/{0}">play</a>'.format(record.get('file')), 
                 record.get('attributes'), 
                 record.get('transcriptions')])

    return template(
        'templates/view', 
        count = database.recordsCount(),
        rows = rows, 
        left = max(skip - limit, 0), 
        right = max(skip + limit, limit))

@route('/soundfiles/<filepath:path>')
def view(filepath):
    return static_file(filepath, root=fileServer.path)

@route('/submit', method='POST')
def submit():
    if request.files.sound and request.files.sound.file:
        model.simpleSubmit(request.forms.items(), request.files.sound.file, fileServer, soundServer, database)
        redirect('/view/0')
    else: 
        return 'sound file is not attached'

@route('/drop')
def drop():
    database.drop()
    redirect('/view/0')

run(host='localhost', port=8080, server='gevent')
