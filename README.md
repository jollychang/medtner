#medtner

Test 3G web app by android and iOS simulator.

```sh
git clone http://code.dapps.douban.com/medtner.git
cd medtner
git submodule init
git submodule update
virtualenv ENV
source ENV/bin/activate
pip install -r pip-req.txt
```

`fab -l`

```
selenium grid2 for testing android and iphone web app
http://code.dapps.douban.com/medtner

Available commands:

    build_iphone_driver      build iphone driver
    create_android_emulator  create and launch android emulator
    install_apk
    launch_ios_simulator     launch ios simulator, fab launch_ios_simulator:sdkLevel,deviceType,videoPath
    register_node            register node to hub
    start_android_service    start android service
    webtests                 run webtests
```
