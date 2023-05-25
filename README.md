# Home Assistant Integration from Timeguard WiFi Switch (non tuya)

This uses the [timeguard-supplymaster-python library](https://github.com/rjpearce/timeguard-supplymaster-python) to connect Home Assistant to your switches. This will make all your Timeguard switches appear as switch entities.

On your Home Assistant install, put the contents of `custom_components/timeguard_switch` into `/config/custom_components/timeguard_switch`, creating the directories if they are not already there.

In `configuration.yaml` add these lines:

```
switch:
  - platform: timeguard_switch
    username: testuser
    password: testpassword
```

Then `Developer Tools` and `Restart` to get it to show up. It make take a while to downloading all the python dependencies before starting up.

