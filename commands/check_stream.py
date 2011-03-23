#!/usr/bin/env python
from twisted.protocols import shoutcast
from twisted.internet import protocol, reactor

PATH = '/stream'
HOST = 'freqbase.com'
PORT = 8080

class ShoutcastBunny(shoutcast.ShoutcastClient):
    userAgent = "Shouty"

    def __init__(self, path="/"):
        self.path = path
        self.got_metadata = False
        self.metaint = None
        self.metamode = "mp3"
        self.databuffer = ""
        self.headers = {}

    def handleHeader(self, key, value):
        if key.lower() == 'icy-metaint':
            self.metaint = int(value)
            self.got_metadata = True
        self.headers[key] = value

    def gotMetaData(self, data):
        for key, value in data:
            if key == 'StreamTitle':
                if 'bunny' in key or 'bunny' in self.headers.values():
                    print 'bunny must be streamin! tune in @ http://freqbase.com/stream.m3u'
                else:
                    print 'bunny pry not streaming :( tune in anywayz i guezz @ http://freqbase.com/stream.m3u'
                reactor.stop()

    def gotMP3Data(self, data):
        pass

    def connectionLost(self, reason):
        pass

protocol.ClientCreator(reactor, ShoutcastBunny, PATH).connectTCP(HOST, PORT)
reactor.run()
