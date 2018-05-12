from sugar.activity import activity
import subprocess


class MetrisActivity(activity.Activity):

    def runFile(self):
        subprocess.call('python ./Metris.py')


Act = MetrisActivity()
Act.runFile()