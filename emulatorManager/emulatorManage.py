import commands
import util
import time
import os
import emulator
from emulator import Emulator

class emulatorManage(object):
    command = None
    emulatorList = []
    
    def __init__(self):
        self.command = util.androidPath() + ' list avd'

    def searchEmulators(self):
        status,result = commands.getstatusoutput(self.command) 
        if status != 0:            
            return None
        for infos in result.split('---------\n'):            
            if infos.find('Name') < 0:
                print 'No emulators.'
                return None
            Name = None
            Path = None
            Target = None
            ABI = None
            Skin = None
            Sdcard = None
            for emulatorinfo in infos.split('\n'):
                subinfo = emulatorinfo.split(': ')
                property = subinfo[0]
                if property.find('Name') > 0:
                    Name = subinfo.pop()
                if property.find('Path') > 0:
                    Path = subinfo.pop()
                if property.find('Target') > 0:
                    Target = subinfo.pop()
                if property.find('ABI') > 0:
                    ABI = subinfo.pop()
                if property.find('Skin') > 0:
                    Skin = subinfo.pop()
                if property.find('Sdcard') > 0:
                    Sdcard = subinfo.pop()
            targets = Target.split(' (')
            target = targets[0]            
            sdkTarget = target.replace('Android ','')                
            emulator = Emulator(Name,Path,Target,ABI,Skin,Sdcard)
            self.emulatorList.append(emulator)
       
    def getAllEmulators(self):
        return self.emulatorList

    def getEmulatorByName(self, emulatorName):
        emuList = []
        for emulator in self.emulatorList:
            if emulator.name == emulatorName:
                emuList.append(emulator)
                return emuList
        return []
    
    def getEmulatorsBySkin(self,width,height):
        emuList = []
        for emulator in self.emulatorList:
            if emulator.skin['width'] == width:
                if emulator.skin['height'] == height:
                    emuList.append(emulator)
        return emuList
              
    def getEmulatorsByLevel(self,level):
        emuList = []
        for emulator in self.emulatorList:
            if emulator.sdkLevel == level:
                emuList.append(emulator)
        return emuList
    
    def getEmulatorsOverLevel(self,level):
        emuList = []
        for emulator in self.emulatorList:
            if emulator.sdkLevel >= level:
                emuList.append(emulator) 
        return emuList

    def startEmulatorList(self):
        if self.emulatorList != []:
            #start the first emulator instead all
            print 'Emulator Name: '+ self.emulatorList[0].name
            print 'SDK Target: '+ self.emulatorList[0].sdkTarget
            print 'SDK level: '+ str(self.emulatorList[0].sdkLevel)
            self.emulatorList[0].startEmulator()

    def stopEmulatorList(self):
        if self.emulatorList != []:
            self.emulatorList[0].stopEmulator()

    def installApkToList(self, apkName):
        if self.emulatorList != []:
            self.emulatorList[0].install(apkName)

    def uninstallApkFromList(self, packageName):
        if self.emulatorList != []:
            self.emulatorList[0].uninstall(apkName)

    def delEmulist(self):
        if self.emulatorList != []:
            for emu in self.emulatorList:
                emu.delete()

    def getDevices(self):
        emuList = []
        device_command = util.adbPath()+' devices'
        status,result = commands.getstatusoutput(device_command)
        if status != 0:
            return emuList
        for info in result.split('List of devices attached\n'):
            name = None
            for emuName in info.split('\n'):
                emuList.append(emuName.split('\t')[0])
        return emuList

    




