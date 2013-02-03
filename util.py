import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

register_openers()

def makeRecord(fileUuid, attributes, transcriptions):
    return {
        'file' : fileUuid,
        'attributes' : attributes,
        'transcriptions' : transcriptions
        }

def postStream(url, params):
    datagen, headers = multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    print urllib2.urlopen(request).read()

