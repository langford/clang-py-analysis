from multiprocessing import Process
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import subprocess
import json
import os
import sys

class JSONServer(object):
    def __init__(self, path = None):
        self.port = 6666
        self.path = path

    def _serve(self, port, path):
        data = []
#        print 'Server', os.getpid()
        address = ('localhost', port)
        listener = Listener(address)
        loop = True
        while loop:
            conn = listener.accept()
            command, payload = conn.recv()
            response_payload = None
            if command == 'OPEN':
                #print command, payload
                path = payload
            elif command == 'WRITE':
                #print command, payload
                data.append(payload)
            elif command == 'FETCH':
                #print command, payload
                response_payload = data
            elif command == 'FLUSH':
                #print command
                json.dump(data, open(path, 'w'))
            elif command == 'CLOSE':
                #print command
                #json.dump(data, open(path, 'w'))
                loop = False
            conn.send(('OK', response_payload))
            conn.close()
        listener.close()
        #print 'DEAD'

    def serve(self):
        #print 'Host', os.getpid()
        self.p = Process(target=self._serve, args=(self.port, self.path))
        self.p.start()
        self.client = JSONClient(self.port)

    def close(self):
        result = self.client.send('FETCH')
        self.client.send('CLOSE')
        self.p.join()
        self.p.terminate()
        #print 'FINISHED'
        return result

    @property
    def environ(self):
        env = os.environ
        env['PORT'] = str(self.port)
        return env

class JSONClient(object):
    def __init__(self, port = None):
        self.port = port
        if not self.port:
            self.port = int(os.environ['PORT'])
    def send(self, command, payload = None):
        address = ('localhost', self.port)
        #print address
        conn = Client(address)
        conn.send((command, payload))
        response, response_payload = conn.recv()
        conn.close()
        return response_payload

    def write(self, payload):
        self.send('WRITE', payload)

if __name__ == '__main__':
    if 'CHILD' in os.environ:
        #print 'Child', os.getpid()
        client = JSONClient()
        client.write({'PID': os.getpid()})
    else:
        server = JSONServer('/Users/schwa/Desktop/test.json')
        server.serve()

        for x in xrange(0, 10):
            env = server.environ
            env['CHILD'] = '1'
            subprocess.call(['python', sys.argv[0]], env = env)
        print server.close()
