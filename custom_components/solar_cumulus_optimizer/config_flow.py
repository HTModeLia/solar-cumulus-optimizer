"""Config flow pour Solar Cumulus Optimizer."""

from typing import Any, Dict, Optional
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from . import DOMAIN


class SolarCumulusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pour Solar Cumulus Optimizer."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Configuration initiale."""
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required("solar_power_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("cumulus_relay_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch")
            ),
            vol.Required("weather_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="weather")
            ),
            vol.Required("linky_ntraf_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("linky_sinti_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)

    async def async_step_reconfigure(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Réconfiguration de l’intégration."""
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            updated_data = {**entry.data, **user_input}
            return self.async_update_reload_and_abort(entry, data_updates=updated_data)

        current_data = dict(entry.data)
        name_default = current_data.get(CONF_NAME, entry.title or "Solar Cumulus Optimizer")

        data_schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required("solar_power_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("cumulus_relay_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch")
            ),
            vol.Required("weather_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="weather")
            ),
            vol.Required("linky_ntraf_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("linky_sinti_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
        })

        suggested_values = {
            CONF_NAME: name_default,
            "solar_power_entity": current_data.get("solar_power_entity"),
            "cumulus_relay_entity": current_data.get("cumulus_relay_entity"),
            "weather_entity": current_data.get("weather_entity"),
            "linky_ntraf_entity": current_data.get("linky_ntraf_entity"),
            "linky_sinti_entity": current_data.get("linky_sinti_entity"),
        }
        data_schema = self.add_suggested_values_to_schema(data_schema, suggested_values)

        return self.async_show_form(step_id="reconfigure", data_schema=data_schema)

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Retourne le flow des options."""
        return SolarCumulusOptionsFlow(config_entry)


class SolarCumulusOptionsFlow(config_entries.OptionsFlow):
    """Options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialisation."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Options principales."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "min_solar_power",
                    default=self.config_entry.options.get("min_solar_power", 500),
                ): vol.All(vol.Coerce(int), vol.Range(min=100, max=5000)),
                vol.Optional(
                    "min_runtime",
                    default=self.config_entry.options.get("min_runtime", 120),
                ): vol.All(vol.Coerce(int), vol.Range(min=30, max=300)),
                vol.Optional(
                    "max_runtime",
                    default=self.config_entry.options.get("max_runtime", 180),
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=480)),
                vol.Optional(
                    "cloud_threshold",
                    default=self.config_entry.options.get("cloud_threshold", 30),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=70)),
                vol.Optional(
                    "hysteresis",
                    default=self.config_entry.options.get("hysteresis", 50),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=200)),
                vol.Optional(
                    "night_temp_threshold",
                    default=self.config_entry.options.get("night_temp_threshold", 5),
                ): vol.All(vol.Coerce(float), vol.Range(min=-10, max=15)),
                vol.Optional(
                    "temp_outside_entity",
                    default=self.config_entry.options.get("temp_outside_entity", ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="temperature",
                    )
                ),
            }),
        )
