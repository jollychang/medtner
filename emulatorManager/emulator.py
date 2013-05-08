import os
import sys
import util
import commands
import sdkManage
import shlex,subprocess

skin_dict = {   'WVGA800':'480x800',
                'WVGA854':'480x854', 
                'QVGA':'240x320', 
                'WQVGA400':'400x240', 
                'WQVGA432':'240x432', 
                'HVGA':'320x480',
                'WXGA':'1280x768',
                'WXGA720':'1280x720', 
                'WXGA800':'1280x800',
                'WSVGA':'1024x600',
                'WXGA800-7in':'1280x800',
             }

class Emulator(object):
    path = None
    sdkTarget = None
    sdkLevel = None
    name = None
    skin = None
    abi = None
    sdcard = None
    port = None

    def __init__(self,Name,Path,Target,ABI,Skin,Sdcard):
        self.name = Name
        self.path = Path
        self.abi = ABI
        self.sdcard = Sdcard
        if Skin != None:
            if Skin in skin_dict:
                Skin = skin_dict[Skin]
            skinpro = Skin.split('x')
            width = skinpro[0]
            height = skinpro[1]
            self.skin = {'width':width,'height':height}
        targets = Target.split('(')
        self.sdkTarget = targets[0]
        levels = targets[1].split(' ')
        self.sdkLevel = levels.pop().replace(')','')
        if self.sdkLevel == None:
            print 'There is no level named '+ self.sdkLevel
            print 'Please run androidManage update and try again' 
            sys.exit()
        if int(self.sdkLevel) >= 14:
            self.abi += '-v7a' 
        
    def printEmulator(self):
        print 'Name: '+self.name
        print 'Path: '+self.path
        print 'Target: '+self.sdkTarget
        print 'ABI: '+self.abi
        print 'Skin: '+self.skin['width']+'x'+self.skin['height']  
        print 'SDKLevel: '+str(self.sdkLevel)
        print '-----------------------\n'

    def createEmulator(self):
        if self.name == None:
            self.name = 'Emulator-'+self.sdkLevel
            print self.name
        sdk_dict = sdkManage.getSDKs()
        sdk_id = None
        echono_command = 'echo no'
        if self.sdkLevel in sdk_dict:
            sdk_id = sdk_dict[self.sdkLevel]
            create_command = util.androidPath()+' create avd -n '+self.name+' -t '+ sdk_id +' --abi '+self.abi 
        if self.path != None:
            create_command += ' -p '+self.path
        if self.skin != None:
            create_command += ' -s '+str(self.skin['width'])+'x'+str(self.skin['height'])
        util.runMultiCommands(echono_command, create_command)

    def deleteEmulator(self):
        if self.name == None:
            return None
        del_command = util.androidPath()+' delete avd -n '+self.name
        util.runcommand(del_command, True)
         
    def startEmulator(self,port=None):
        port_command = ''
        self.port = port
        if self.port != None:
            if self.port%2 != 0 or self.port<5554 or self.port>5584 :
                print 'InputError:port number must be an even integer between 5554 and 5584'
                return None
            port_command = ' -port '+self.port
        start_command = util.emulatorPath() + ' -avd ' + self.name + port_command
        util.osrun(start_command)
        #util.runcommand(start_command, True)
    
    def stopEmulator(self):
        port = self.getDevices()
        if port == []:
            print 'No emulator launched.'
        else:
            stop_command_default = util.adbPath()+' -s ' + port[0] + ' emu kill'
            util.runcommand(stop_command_default, True)
            print 'Stop emulator:'+port[0]
    
    def startEmulatorWithOptions(self,opt):
        self.port = opt.get('-port')
        coms = ' '
        for prop in opt:
            coms = com+prop+' '+opt[prop]+' '
        start_command = util.emulatorPath() + ' -avd ' + self.name + coms 
        util.runcommand(start_command, True)

    def getDevices(self):
        emuList = []
        device_command = util.adbPath()+' devices'
        util.runcommand(device_command, True)
        status,result = commands.getstatusoutput(device_command)
        if status != 0:
            return emuList
        for info in result.split('\n'):
            for emuName in info.split('\t'):
                if emuName.startswith('emulator') > 0:
                    emuList.append(emuName) 
        return emuList
    
    def restartadb(self):
        kill_command = util.adbPath() + ' kill-server'
        start_command = util.adbPath() + 'start-server'
        util.runcommand(kill_command, True)
        util.runcommand(start_command, True)
            
def install(apkName):
    install_command = util.adbPath() + ' -e install -r ' + apkName
    util.runcommand(install_command, True)
    
def uninstall(packageName):
    uninstall_command = util.adbPath() + ' -e uninstall ' + packageName
    util.runcommand(uninstall_command, True)
    
def startService(activityName):
    print 'Start intent...'
    start_command = util.adbPath()+' shell am start -a android.intent.action.MAIN -n '+activityName 
    util.runcommand(start_command,True)
    print 'Forward tcp:7000 tcp:8080...'
    tcp_command = util.adbPath() +' forward tcp:7000 tcp:8080'
    util.osrun(tcp_command)
    print 'Socat TCP-LISTEN:7001,fork TCP:localhost:7000...'
    socat_command = 'socat TCP-LISTEN:7001,fork TCP:localhost:7000'
    util.osrun(socat_command)
    

    
