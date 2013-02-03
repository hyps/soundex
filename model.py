import uuid
import shutil
import random
import string
import util

class FileServer:
    def __init__(self, path, saveToDisk = True):
        self.path = path
        self.saveToDisk = saveToDisk
        
    def storeFile(self, inputStream):
        fileUuid = str(uuid.uuid1());

        if self.saveToDisk:
            with open(self.path + fileUuid, 'wb') as outBuf:
                shutil.copyfileobj(inputStream, outBuf, 16*1024);

        return fileUuid

    def filePath(self, fileUuid):
        return self.path + fileUuid


class SoundServer:
    def __init__(self, analyze = True):
        self.analyze = analyze
        
    def analyzeSound(self, inputStream):
        length = 16*1024
        seed = 0
        
        if self.analyze:
            # this may be slow during noise generation, need put it into C
            while True:
                buf = inputStream.read(length)
                for vl in buf:
                    seed = seed + ord(vl)
                if not buf:
                    break
        else: seed = random.randint(1, 10)
                
        #random.seed(seed)
        result = []
        
        for tr in range(1 + seed % 5):
            result.append(
                {
                    'value': ''.join(random.sample(string.lowercase, random.randint(3, 7))),
                    'confidence': random.randint(1, 10)
                })
            
        return result


class Database:
    def __init__(self, connection, database_name):
        self.connection = connection
        self.database = self.connection[database_name]
        self.transcripts = self.database.transcripts

    def storeRecord(self, fileUuid, attributes, transcript):
        return self.transcripts.insert(
            {
                'file' : fileUuid,
                'attributes' : attributes,
                'transcriptions' : transcript
            })
            
    def getRecords(self, skip, limit):
        try:
            return self.transcripts.find().skip(skip).limit(limit)
        except:
            return []

    def recordsCount(self):
        return self.transcripts.find().count()

    def drop(self):
        self.connection.drop_database(self.database)

def simpleSubmit(attributes, soundfile, fileServer, soundServer, database):
    soundfile.seek(0)
    fileUuid = fileServer.storeFile(soundfile)
    soundfile.seek(0)
    transcript = soundServer.analyzeSound(soundfile)
    return str(database.storeRecord(fileUuid, attributes, transcript))


