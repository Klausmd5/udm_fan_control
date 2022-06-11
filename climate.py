"""Adds support for generic thermostat units."""
import logging
import json
from datetime import timedelta
from homeassistant.components.climate import SUPPORT_FAN_MODE
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_FAN_ONLY,
)
from homeassistant.const import (
    TEMP_CELSIUS,
)
from homeassistant.core import DOMAIN as HA_DOMAIN, callback
from .const import DOMAIN

from .UdmAPI import FAN_AUTO, FAN_LOW, FAN_HIGH, FAN_MEDIUM, FAN_MIDDLE, UdmAPI

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    entries = []
    api = hass.data[DOMAIN][entry.entry_id]

    entries.append(UDMFanControl(api, hass))

    async_add_entities(entries)


class UDMFanControl(ClimateEntity):
    """Representation of a Climate."""

    def __init__(self, api: UdmAPI, hass) -> None:
        self._api = api
        self._hass = hass
        self._attr_name = "udm_fan"
        self._attr_hvac_mode = HVAC_MODE_FAN_ONLY
        self._attr_hvac_modes = HVAC_MODE_FAN_ONLY
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_supported_features = SUPPORT_FAN_MODE
        self._attr_fan_modes = [FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_MIDDLE]
        self._attr_fan_mode = FAN_AUTO

        self._attr_current_temperature = self._api.update()

    def set_fan_mode(self, fan_mode):
        self._api.setTemp(fan_mode)
        _LOGGER.info("fan_mode: %s", fan_mode)

    async def async_set_fan_mode(self, fan_mode):
        self._api.setTemp(fan_mode)
        _LOGGER.info("fan_mode: %s", fan_mode)
