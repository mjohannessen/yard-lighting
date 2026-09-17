"""
Zone -> serial port mapping, MQTT broker address, and topic prefixes.
bridge.py must not hardcode port names or topic strings — add them here.
"""

# Mosquitto runs on this Pi, not the Mac Mini.
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

SERIAL_BAUD = 115200

# Stable names from /etc/udev/rules.d/99-garden-picos.rules, not raw
# /dev/ttyACMn (enumeration order can shift on reboot).
ZONE_SERIAL_PORTS = {
    1: "/dev/ttyPICO1",
    2: "/dev/ttyPICO2",
    3: "/dev/ttyPICO3",
    4: "/dev/ttyPICO4",
}

TOPIC_ZONE_SET = "garden/lights/zone/{zone}/set"
TOPIC_ZONE_STATUS = "garden/lights/zone/{zone}/status"
TOPIC_ALL_SET = "garden/lights/all/set"
TOPIC_SCENE_SET = "garden/lights/scene/set"
