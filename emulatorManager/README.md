##使用说明

###确保环境变量中有ANDROID_HOME
###建议将androidManage加入环境变量，方便使用

**参数说明如下**
androidManage [action] [option]

    [action]            [option]
    1)avdlist           -a              查看所有模拟器的信息
                        -n <name>       查看名称为<name>的模拟器具体信息
                        -s <skin>       查看分辨率为<skin>的模拟器具体信息，skin的输入格式为wwwxhhh，如400x800
                        -l <level>      查看SDKlevel版本为<level>的模拟器具体信息
                        -o <level>      查看版本高于<level>的模拟器具体信息

    2)avdstart          -n <name>       启动名称为<name>的模拟器
                        -s <skin>       启动一个分辨率为<skin>的模拟器
                        -l <level>      启动一个版本为<level>的模拟器
                        -o <level>      启动一个版本高于<level>的模拟器
    
    3)avdstop                           关闭当前启动的模拟器(有多个时关闭端口号最小的)

    4)avddel            -a              删除所有模拟器
                        -n <name>       删除名称为<name>的模拟器
                        -s <skin>       删除分辨率为<skin>的模拟器，skin的输入格式为wwwxhhh，如480x800
                        -l <level>      删除SDKlevel版本为<level>的模拟器
                        -o <level>      删除版本高于<level>的模拟器
    
    5)install <apkName>                 安装apk到当前运行的模拟器中

    6)uninstall <packageName>           卸载模拟器中的app，<package>为app的包名，如com.douban.group

    7)update                            更新SDK，需要耐心等待
    
    8)service <WebDriver-apkName>       安装apk并启动selenium android service



 

