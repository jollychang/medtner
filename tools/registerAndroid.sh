#!/bin/bash

HUB_HOST="localhost"
HUB_PORT="4444"
LOCAL_IP="10.0.2.83"
SOCAT_PORT="7001"
PLATFORM='ANDROID'
BROWSERNAME='android'
MAXINSTANCES=1

JSON="{'configuration': {'registerCycle': 5000, 'hub': 'http://<HUB_HOST>:<HUB_PORT>/grid/register', 'host': '<LOCAL_IP>', 'proxy': 'org.openqa.grid.selenium.proxy.DefaultRemoteProxy', 'maxSession': 1, 'port': <SOCAT_PORT>, 'hubPort': <HUB_PORT>, 'hubHost': '<HUB_HOST>', 'url': 'http://<LOCAL_IP>:<SOCAT_PORT>', 'remoteHost': 'http://<LOCAL_IP>:<SOCAT_PORT>', 'register': true, 'role': 'node'}, 'class': 'org.openqa.grid.common.RegistrationRequest', 'capabilities': [{'seleniumProtocol': 'WebDriver', 'platform': '<PLATFORM>', 'browserName': '<BROWSERNAME>', 'version': null, 'maxInstances': <MAXINSTANCES>}]}"
JSON=${JSON//<HUB_HOST>/$HUB_HOST}
JSON=${JSON//<HUB_PORT>/$HUB_PORT}
JSON=${JSON//<LOCAL_IP>/$LOCAL_IP}
JSON=${JSON//<SOCAT_PORT>/$SOCAT_PORT}
JSON=${JSON//<PLATFORM>/$PLATFORM}
JSON=${JSON//<BROWSERNAME>/$BROWSERNAME}
JSON=${JSON//<MAXINSTANCES>/$MAXINSTANCES}

echo json is: ${JSON}
curl -X POST -d "${JSON}" http://$HUB_HOST:$HUB_PORT/grid/register