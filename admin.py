import model
import sys
import random
import string
import config

def fillWithNoise():
    fileServer = model.FileServer('', False)
    soundServer = model.SoundServer(False)
    database = model.Database(config.mongoConnect(), config.mongoDatabaseName())
    with open("white_noise.ogg", "rb") as soundfile:
        for i in range(1000000):
            model.simpleSubmit(
                {
                    'attribute1': ''.join(random.sample(string.lowercase, random.randint(3, 7))),
                    'attribute2': ''.join(random.sample(string.lowercase, random.randint(3, 7)))
                },
                soundfile, 
                fileServer, 
                soundServer, 
                database)

def drop():
    database = model.Database()
    database.drop()

if len(sys.argv) > 1:
   globals()[sys.argv[1]]()
else:
    print 'Available actions:'
    print 'fillWithNoise'
    print 'drop'
