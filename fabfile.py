# -*- coding: utf-8 -*-
'''
selenium grid2 for testing android and iphone web app
http://code.dapps.douban.com/medtner
'''
from fabric.api import local, task

@task
def webtests():
	'''run webtests'''
	local("pybot ./webtests/test_base.txt")

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

@taks
def create_android_emulator():
	'''create android emulator'''
	local("android create avd -n my_android -t 12 -c 100M")
	local("emulator -avd my_android &")