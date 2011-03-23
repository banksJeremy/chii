#!/usr/bin/env python
from twisted.protocols import shoutcast
from twisted.internet import protocol, reactor

PATH = '/stream'
HOST = 'freqbase.com'
PORT = 8080

class ShoutcastBunny(shoutcast.ShoutcastClient):
    def gotMetaData(self, data):
        for key, value in data:
            if key == 'StreamTitle':
                if 'bunny' in key:
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
