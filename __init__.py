import logging
import socket
import time

import voluptuous as vol

from homeassistant.const import CONF_COMMAND
import homeassistant.helpers.config_validation as cv

DOMAIN = "ir_sender"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_COMMAND): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_IP = "iTach057F21.lh.site.vionox.net"
DEVICE_PORT = 4998

def setup(hass, config):
    """Set up the IR Sender service."""

    def send_ir_command(call):
        """Send the IR command."""
        ir_command = call.data.get(CONF_COMMAND)
        device_ip = call.data.get("device_ip", DEFAULT_DEVICE_IP)

        if not ir_command:
            _LOGGER.error("No IR command provided.")
            return

        try:
            with socket.create_connection((device_ip, DEVICE_PORT), timeout=5) as s:
                s.sendall((ir_command + "\r\n").encode())
        except Exception as e:
            _LOGGER.error(f"Failed to send IR command to {device_ip}. Error: {e}")

    hass.services.register(DOMAIN, "send", send_ir_command)

    return True
