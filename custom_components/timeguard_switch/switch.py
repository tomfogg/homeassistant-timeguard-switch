"""Platform for light integration."""
from __future__ import annotations

from timeguard_supplymaster import Client, Mode

import logging
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv

from homeassistant.components.switch import (SwitchEntity, PLATFORM_SCHEMA)
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    username = config[CONF_USERNAME]
    password = config.get(CONF_PASSWORD)

    # Setup connection with devices/cloud
    try:
        hub = Client(use_config_file=False, api_username=username, api_password=password, quiet=True)
        devices = hub.refresh_devices()
    except Exception as e:
        _LOGGER.error("Could not connect to Timeguard "+str(e))
        return

    # Add devices
    add_entities(TimeguardSwitch(switch) for switch in devices)

class TimeguardSwitch(SwitchEntity):

    def __init__(self, switch) -> None:
        self._switch = switch
        self._attr_unique_id = switch.id

    @property
    def is_on(self):
        return self._switch.mode == Mode.ON

    @property
    def name(self):
        return self._switch.name

    def turn_on(self, **kwargs) -> None:
        self._switch.set_mode(Mode.ON)

    def turn_off(self, **kwargs) -> None:
        self._switch.set_mode(Mode.OFF)

    def update(self) -> None:
        self._switch.refresh_device_info()
