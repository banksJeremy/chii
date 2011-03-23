import os, subprocess
from chii import command

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_stream.py')

@command
def bunny(self, channel, *args):
    self.msg_deferToThread(channel, subprocess.check_output, ['python', PATH])
