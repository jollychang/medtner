import sys
import os,os.path
import shlex,subprocess

def getEnvByName(envName):
    envHome = None
    try:
        envHome = os.environ[envName]
    except Exception, e:
        print 'make sure $ANDROID_HOME is in profile file'
        raise e
    return envHome

def androidPath():
    androidHome = getEnvByName('ANDROID_HOME')
    androidPath = os.path.join(androidHome,'tools/android')
    return androidPath

def emulatorPath():
    emulatorHome = getEnvByName('ANDROID_HOME')
    emulatorPath = os.path.join(emulatorHome,'tools/emulator')
    return emulatorPath

def adbPath():
    adbHome = getEnvByName('ANDROID_HOME')
    adbPath = os.path.join(adbHome, 'platform-tools/adb')
    return adbPath

def osrun(commandline):
    commandline += ' &'
    os.system(commandline)

def runcommand(commandline,printlog):
    args = shlex.split(commandline)
    p = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    while True:
        line = p.stdout.readline()
        if printlog == True:
            print line,
        else:
            print '.',
        if not line:
            break

def runMultiCommands(cmd1, cmd2):
    args1 = shlex.split(cmd1)
    args2 = shlex.split(cmd2)
    p1 = subprocess.Popen(args1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(args2, stdin=p1.stdout)
    p1.stdout.close()
    p2.communicate()[0]

