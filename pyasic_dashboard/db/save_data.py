import argparse
import asyncio
from pyasic import get_miner
from pyasic_dashboard.db import write_data


parser = argparse.ArgumentParser(description="Save miner data")
parser.add_argument("ip", type=str, help="miner IP address")
parser.add_argument(
    "data_file",
    type=str,
    nargs="?",
    default="miner_data.db",
    help="File path to save the data (csv or sqlite)",
)
parser.add_argument("sleep_mins", type=int, help="Sleep interval (minutes)")
args = parser.parse_args()


async def main():
    miner = await get_miner(args.ip)
    await write_data(miner=miner, data_file=args.data_file, sleep_mins=args.sleep_mins)


if __name__ == "__main__":
    # python save_data.py 192.168.0.161 miner_data.db 1
    asyncio.run(main())
