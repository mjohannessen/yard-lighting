"""
asyncio MQTT<->serial bridge. Forwards zone/all/scene MQTT commands to
each zone's Pico over serial, and forwards each Pico's status lines back
to its MQTT status topic. Intentionally dumb: no schedules, scenes, or
automation logic here — that's openHAB's job.
"""
import asyncio
import json
import logging

import aiomqtt
import serial_asyncio

import config

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bridge")


class ZoneLink:
    def __init__(self, zone: int, port: str):
        self.zone = zone
        self.port = port
        self.reader = None
        self.writer = None
        self.last_payload = None

    async def connect(self):
        while self.writer is None:
            try:
                self.reader, self.writer = await serial_asyncio.open_serial_connection(
                    url=self.port, baudrate=config.SERIAL_BAUD
                )
                log.info("zone %d: connected on %s", self.zone, self.port)
            except OSError:
                log.warning("zone %d: %s not ready yet, retrying", self.zone, self.port)
                await asyncio.sleep(2)

    async def send(self, payload: dict):
        self.last_payload = payload
        if self.writer is None:
            return
        try:
            self.writer.write((json.dumps(payload) + "\n").encode())
            await self.writer.drain()
        except OSError:
            log.warning("zone %d: write failed, will reconnect", self.zone)
            self.reader = None
            self.writer = None

    async def keepalive_loop(self):
        """Repeat the last command so the Pico's contact watchdog doesn't
        fire between openHAB commands. Not a decision, just a repeat —
        the Pico ignores an identical command other than resetting its
        watchdog."""
        while True:
            await asyncio.sleep(config.KEEPALIVE_INTERVAL_S)
            if self.last_payload is not None:
                await self.send(self.last_payload)

    async def status_loop(self, mqtt_client: aiomqtt.Client):
        topic = config.TOPIC_ZONE_STATUS.format(zone=self.zone)
        while True:
            if self.reader is None:
                await self.connect()
            try:
                line = await self.reader.readline()
            except OSError:
                line = b""
            if not line:
                log.warning("zone %d: serial connection dropped, reconnecting", self.zone)
                self.reader = None
                self.writer = None
                continue
            await mqtt_client.publish(topic, payload=line.strip())


def _zone_for_topic(topic, zones):
    for zone in zones:
        if topic == config.TOPIC_ZONE_SET.format(zone=zone):
            return zone
    return None


async def run(zones):
    async with aiomqtt.Client(config.MQTT_BROKER, port=config.MQTT_PORT) as client:
        await client.subscribe(config.TOPIC_ALL_SET)
        await client.subscribe(config.TOPIC_SCENE_SET)
        for zone in zones:
            await client.subscribe(config.TOPIC_ZONE_SET.format(zone=zone))

        status_tasks = [asyncio.create_task(link.status_loop(client)) for link in zones.values()]
        try:
            await _forward(client, zones)
        finally:
            for task in status_tasks:
                task.cancel()


async def _forward(client, zones):
    async for message in client.messages:
        try:
            payload = json.loads(message.payload)
        except (ValueError, TypeError):
            log.warning("dropping malformed payload on %s", message.topic)
            continue

        topic = str(message.topic)
        if topic in (config.TOPIC_ALL_SET, config.TOPIC_SCENE_SET):
            await asyncio.gather(*(link.send(payload) for link in zones.values()))
            continue

        zone = _zone_for_topic(topic, zones)
        if zone is not None:
            await zones[zone].send(payload)


async def main():
    # Zone links (and their keepalives) outlive any one MQTT connection,
    # so zones hold their last command through a broker restart. Each
    # zone's status_loop opens its own serial port, so an unplugged Pico
    # doesn't stop the other zones from connecting.
    zones = {zone: ZoneLink(zone, port) for zone, port in config.ZONE_SERIAL_PORTS.items()}
    for link in zones.values():
        asyncio.create_task(link.keepalive_loop())

    while True:
        try:
            await run(zones)
        except aiomqtt.MqttError:
            log.warning("MQTT connection lost, reconnecting in 5s")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
