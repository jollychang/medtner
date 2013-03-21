# -*- coding: utf-8 -*-
'''
selenium grid2 for testing android and iphone web app
http://code.dapps.douban.com/medtner
'''
import os
from fabric.api import local, task, cd

@task
def webtests(platform='android'):
    '''run webtests'''
    local("pybot -v PLATFORM:%s ./webtests/test_base.txt" % platform)

@task
def start_android_service():
    '''start android service'''
    #local("wget http://selenium.googlecode.com/files/android-server-2.21.0.apk")
    #local("adb -s emulator-5554 -e install -r android-server-2.21.0.apk ")
    #local("adb shell am start -a android.intent.action.MAIN -n org.openqa.selenium.android.app/.MainActivity  -e debug true")
    local("adb shell am start -a android.intent.action.MAIN -n org.openqa.selenium.android.app/.MainActivity")
    local("adb forward tcp:8080 tcp:8080 &")

@task
def install_apk():
    local("adb install -r ./libs/android-server-2.6.0.apk")

@task
def create_android_emulator():
    '''create android emulator'''
    local("echo no | android -s create avd --force --name my_android --target 1 --sdcard 100M")
    local("emulator -avd my_android &")

@task()
def build_iphone_driver(selenium_path='/Users/jollychang/Work/selenium'):
    '''build iphone driver'''
    with cd(selenium_path):
        sdk = local("xcodebuild -showsdks |grep iphonesimulator | awk '{print $6}'", capture=True)
        project_path = os.path.join(selenium_path, 'iphone/iWebDriver.xcodeproj')
        local("/usr/bin/xcodebuild -project %s clean build -sdk %s -target iWebDriver -configuration Debug" % (project_path, sdk))

@task(pty=False)
def launch_ios_simulator():
    '''launch ios simulator'''
    local("sudo -ujollychang /usr/bin/instruments -t /Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.bundle/Contents/Resources/Automation.tracetemplate  /Users/jollychang/Work/selenium/iphone/build/Debug-iphonesimulator/iWebDriver.app > output 2> /dev/null < /dev/null &")

@task
def register_node(platform="android", hubhost="qa-shire-rc.intra.douban.com"):
    '''register node to hub'''
    if platform == "android":
        cmd = "flynnid --nodeport=8080 --browsername=android --browserver=3.1 --platform=ANDROID  --hubhost=%s" % hubhost
    elif platform == "iphone" or "ios":
        cmd = "flynnid --nodeport=3001 --browsername=iphone --browserver=6.1 --platform=ANY  --hubhost=%s" % hubhost
    local(cmd)
