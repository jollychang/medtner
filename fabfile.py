# -*- coding: utf-8 -*-
'''
selenium grid2 for testing android and iphone web app
https://github.com/jollychang/medtner
'''
import os
from fabric.api import local, task, cd
from EmulatorManager.sdkManage import getLastSDKLevel

current_path = os.path.dirname(os.path.abspath(__file__))
android_manage = os.path.join(current_path, "/EmulatorManager/androidManage")
SELENIUM_HUB_HOST = "qa-shire-rc.intra.douban.com"
IOS_WEBDRIVER_HUB = "http://localhost:3001/wd/hub"
ANDROID_WEBDRIVER_HUB = "http://localhost:8080/wd/hub"
IOS_WEBDRIVER_NODE_PORT = "3001"
ANDROID_WEBDRIVER_NODE_PORT = "8080"



def _get_env_by_name(env_name):
    try:
        env_value = os.environ[env_name]
    except Exception, e:
        print 'make sure $ANDROID_HOME is in profile file'
        raise e
    return env_value

def _adb_path():
    adb_home_path = _get_env_by_name('ANDROID_HOME')
    adb_bin_path = os.path.join(adb_home_path, 'platform-tools/adb')
    return adb_bin_path

@task
def webtests(platform="android"):
    '''run webtests'''
    if platform == 'ios':
        local("pybot -v PLATFORM:%s -v IPHONE:%s ./webtests/test_base.txt" % (platform, IOS_WEBDRIVER_HUB))
    else:
        local("pybot -v PLATFORM:%s -v ANDROID:%s ./webtests/test_base.txt" % (platform, ANDROID_WEBDRIVER_HUB))
        
@task
def start_android_service():
    '''start android service'''
    print 'Start intent...'
    start_command = _adb_path() +' shell am start -a android.intent.action.MAIN -n '+ 'org.openqa.selenium.android.app/.MainActivity' 
    local(start_command, True)
    print 'Forward tcp:7000 tcp:8080...'
    tcp_command = _adb_path() +' forward tcp:7000 tcp:8080'
    local(tcp_command)
    print 'Socat TCP-LISTEN:7001,fork TCP:localhost:7000...'
    socat_command = 'socat TCP-LISTEN:7001,fork TCP:localhost:7000'
    local(socat_command)

@task
def install_apk():
    dir_name = os.path.join(current_path, "/libs/") 
    file_name = "android-server-2.6.0"
    file_suffix = "apk"
    android_server_apk_path = os.path.join(dir_name, file_name + "." + file_suffix)
    command = "%s install %s" % (android_manage, android_server_apk_path)
    local(command)

@task
def create_android_emulator(level=None):
    '''create and launch android emulator'''
    if level == None:
        level = getLastSDKLevel()['level']
    command = "%s avdstart -l %s &" % (android_manage, str(level))
    local(command)

@task()
def build_iphone_driver(selenium_path='/Users/jollychang/Work/selenium'):
    '''build iphone driver'''
    with cd(selenium_path):
        sdk = local("xcodebuild -showsdks |grep iphonesimulator | awk '{print $6}'", capture=True)
        project_path = os.path.join(selenium_path, 'iphone/iWebDriver.xcodeproj')
        local("/usr/bin/xcodebuild -project %s clean build -sdk %s -target iWebDriver -configuration Debug" % (project_path, sdk))

@task(pty=False)
def launch_ios_simulator(sdkLevel="", deviceType="", videoPath=""):
    '''launch ios simulator, fab launch_ios_simulator:sdkLevel,deviceType,videoPath'''
    options = " ";
    if sdkLevel: 
        options = options + " -s " + sdkLevel
    if deviceType:
        options = options + " -f " +  deviceType
    if videoPath:
        options  = options +" -v " + videoPath
    local("./libs/waxsim"+ options +" ./libs/iWebDriver.app &  ")

@task
def register_node(platform="android", hubhost=SELENIUM_HUB_HOST, webdriver_node_port=ANDROID_WEBDRIVER_NODE_PORT):
    '''register node to hub'''
    if platform == "android":
        cmd = "flynnid --nodeport=%s --browsername=android --browserver=3.1 --platform=ANDROID  --hubhost=%s" % (webdriver_node_port, hubhost)
    elif platform == "iphone" or "ios":
        cmd = "flynnid --nodeport=%s --browsername=iphone --browserver=6.1 --platform=ANY  --hubhost=%s" % (webdriver_node_port, hubhost)
    local(cmd)
