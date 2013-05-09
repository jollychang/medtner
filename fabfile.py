# -*- coding: utf-8 -*-
'''
selenium grid2 for testing android and iphone web app
http://code.dapps.douban.com/medtner
'''
import os, sys
from fabric.api import local, task, cd
from EmulatorManager.sdkManage import getLastSDKLevel

current_path = sys.path[0]
tool_path = current_path + '/EmulatorManager/androidManage'

@task
def webtests(platform='android'):
    '''run webtests'''
    if platform == ios:
        local("pybot -v PLATFORM:%s -v IPHONE:http://iosci.intra.douban.com:3001/wd/hub ./webtests/test_base.txt" % platform)
    else:
        local("pybot -v PLATFORM:%s -v ANDROID:http://iosci.intra.douban.com:7001/wd/hub ./webtests/test_base.txt" % platform)
        
@task
def start_android_service():
    '''start android service'''
    #local("wget http://selenium.googlecode.com/files/android-server-2.21.0.apk")
    #local("adb -s emulator-5554 -e install -r android-server-2.21.0.apk ")
    #local("adb shell am start -a android.intent.action.MAIN -n org.openqa.selenium.android.app/.MainActivity  -e debug true")
    '''
    local("adb shell am start -a android.intent.action.MAIN -n org.openqa.selenium.android.app/.MainActivity")
    local("adb forward tcp:7000 tcp:8080 &")
    local("socat TCP-LISTEN:7001,fork TCP:localhost:7000")
    '''
    command = tool_path+' service '
    local(command)

@task
def install_apk():
    '''
    local("adb install -r ./libs/android-server-2.6.0.apk")
    '''
    command = tool_path+' install '+current_path+'/libs/android-server-2.6.0.apk'
    local(command)

@task
def create_android_emulator(level=None):
    '''create and launch android emulator'''
    #local("echo no | android -s create avd --force --name my_android --target 1 --sdcard 100M")
    #local("emulator -avd my_android &")
    if level == None:
        level = getLastSDKLevel()['level']
    command = tool_path+' avdstart -l '+str(level)+' &'
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
def register_node(platform="android", hubhost="qa-shire-rc.intra.douban.com"):
    '''register node to hub'''
    if platform == "android":
        cmd = "flynnid --nodeport=8080 --browsername=android --browserver=3.1 --platform=ANDROID  --hubhost=%s" % hubhost
    elif platform == "iphone" or "ios":
        cmd = "flynnid --nodeport=3001 --browsername=iphone --browserver=6.1 --platform=ANY  --hubhost=%s" % hubhost
    local(cmd)
