import util
import sys
import commands

def getSDKs():
    sdk_dict = {}
    commandline = util.androidPath()+' list target'
    status,result = commands.getstatusoutput(commandline)
    if status != 0:
        return None
    for infos in result.split('---------\n'):
        localID = None
        level = None
        for sdkinfo in infos.split('\n'):
            propertys = sdkinfo.split(': ')[0]
            if propertys.endswith('id'):
                sdklevel = sdkinfo.split(': ')[1]
                localID = sdklevel.split(' or ')[0]
                level1 = sdklevel.split(' or ')[1]
                level1 = level1.replace('"','')
                if level1.startswith('android'):
                    level = level1.replace('android-','')
                    sdk_dict[level] = localID
    #for i in sdk_dict:
        #print  i+':'+sdk_dict[i] 
    return sdk_dict
   
def getTarget(level):
    id_dict = {}
    commandline = util.androidPath()+' list targets'
    status,result = commands.getstatusoutput(commandline)
    if status != 0:
        return None
    for infos in result.split('---------\n'):
        name = None
        sdk_level = None
        for sdkinfo in infos.split('\n'):
            propertys = sdkinfo.split(': ')[0]
            if propertys.endswith('API level'):
                sdk_level = sdkinfo.split(': ')[1] 
            if propertys.endswith('Name'):
                android_name = sdkinfo.split(': ')[1]
                if android_name.startswith('Android '):
                    name = android_name.replace('Android ', '') 
            id_dict[sdk_level] = name 
    #for i in id_dict:
        #print 'dict[%s]='% i,id_dict[i] 
    #print 'level '+level
    if level not in id_dict:
        print 'There is no level named '+level
        sys.exit()
    return id_dict[level]

def getLastSDKLevel():
    sdks_dict = getSDKs()
    lastkey = 0
    for key in sdks_dict:
        if key == None:
            lastkey = int(key)
        else:
            if lastkey < int(key):
                lastkey = int(key)
    return {'id':sdks_dict[str(lastkey)],'level':lastkey}

def updateSDK():
    update_command = util.androidPath() + ' -v update sdk -s -a -f -u'
    util.runcommand(update_command, True)

