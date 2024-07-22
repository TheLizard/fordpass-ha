import pytest
from unittest.mock import patch, MagicMock

from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME

from homeassistant.data_entry_flow import FlowResultType

from custom_components.fordpass.const import CONF_DISTANCE_UNIT, CONF_PRESSURE_UNIT, DOMAIN, REGION, REGIONS

async def test_validate_config_flow(hass: HomeAssistant):
    """ Test the config flow """
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "user"

    with patch(
        "custom_components.fordpass.async_setup", return_value=True
    ) as mock_setup, patch(
        "custom_components.fordpass.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry, patch("custom_components.fordpass.async_unload_entry",
        return_value=True,
    ) as mock_unload_entry:
        # Pick any region from the list of regions
        region = list(REGIONS.keys())[0]
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "fordpass-ha@github.com",
                REGION: region
            },
        )

        assert result2["type"] == FlowResultType.FORM
        assert result2["errors"] == {}
        assert result2["step_id"] == "token"

        #print(result2)
        # Extract the URL from data_schema
        #URL = result2["data_schema"](data={"tokenstr": "dummy"})
        #print(data)

    # Test API with an empty tokenstr
    result3 = await hass.config_entries.flow.async_configure(
        result2["flow_id"],
        {
            CONF_URL: "",
            "tokenstr": ""
        },
    )

    assert result3["type"] == FlowResultType.FORM
    assert result3["errors"] == {'base': 'invalid_token'}
    assert result3["step_id"] == "token"
