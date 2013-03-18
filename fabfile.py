'''
selenium grid2 for testing android and iphone web app
http://code.dapps.douban.com/medtner
'''
from fabric.api import local, task

@task
def webtests():
	'''run webtests'''
	local("pybot ./webtests/test_base.txt")