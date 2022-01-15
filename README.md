# medtner

Use [selenium Grid2](https://code.google.com/p/selenium/wiki/Grid2) for testing web app by android and iOS simulator.    


## Dependence
* [socat](http://www.dest-unreach.org/socat/)

##I nstall

>git clone https://github.com/jollychang/medtner.git    
cd medtner    
virtualenv ENV    
source ENV/bin/activate    
pip install -r pip-req.txt    


## Usage
`fab -l`

```
Use selenium Grid2 for testing web app by android and iOS simulator.
https://github.com/jollychang/medtner

Available commands:

    build_iphone_driver      build iphone driver
    create_android_emulator  create and launch android emulator
    install_apk
    launch_ios_simulator     launch ios simulator, fab launch_ios_simulator:sdkLevel,deviceType,videoPath
    register_node            register node to hub
    start_android_service    start android service
    webtests                 run webtests
```


[Android and iOS Support](http://seleniumhq.wordpress.com/2013/12/24/android-and-ios-support)
