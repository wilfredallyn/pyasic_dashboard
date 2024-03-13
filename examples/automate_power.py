import asyncio
from datetime import datetime, timedelta
from pyasic import get_miner
from pyasic.miners.base import BaseMiner
from typing import List


async def automate_daily_power_changes(
    miner: BaseMiner, power_settings: List[dict]
):
    """
    Example:
        power_settings = [
            { "hour": 6, "power": 300},  # 6AM: 300W
            { "hour": 21, "power": 1000},  # 9PM: 1000W
        ]
    """
    power_settings = sorted(power_settings, key=lambda x: x["hour"])

    while True:
        now = datetime.now()
        found_next_setting = False

        for setting in power_settings:  # Schedule next setting
            hour = setting["hour"]
            power = setting["power"]
            if now.replace(hour=hour, minute=0, second=0, microsecond=0) > now:
                next_change_time = now.replace(
                    hour=hour, minute=0, second=0, microsecond=0
                )
                found_next_setting = True
                break
        if not found_next_setting:  # Schedule first setting for next day
            first_setting_hour = power_settings[0]["hour"]
            first_setting_power = power_settings[0]["power"]
            next_change_time = now.replace(
                hour=first_setting_hour, minute=0, second=0, microsecond=0
            ) + timedelta(days=1)
            power = first_setting_power

        seconds_until_next_change = (next_change_time - now).total_seconds()

        if seconds_until_next_change > 0:
            await asyncio.sleep(seconds_until_next_change)

        await miner.set_power_limit(power)


async def main():
    ip = "192.168.0.100"
    power_settings = [
        { "hour": 6, "power": 300},  # 6AM: 300W
        { "hour": 21, "power": 1000},  # 9PM: 1000W
    ]
    miner = await get_miner(ip)
    await automate_daily_power_changes(miner, power_settings)


if __name__ == "__main__":
    asyncio.run(main())
