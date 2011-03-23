import os, subprocess
from chii import command

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_stream.py')

@command
def bunny(self, channel, *args):
    """checks whetha bunny is streamin'"""
    return subprocess.check_output(['python', PATH])
