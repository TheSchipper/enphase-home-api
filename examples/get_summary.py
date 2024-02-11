import aiohttp
import asyncio

from enphase_home_api_client.enphase import EnphaseAPIClient


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        summary = await EnphaseAPIClient().get_system_summary_from_enphase(session)
        devices = await EnphaseAPIClient().get_system_devices_from_enphase(session)
        sys_info = await EnphaseAPIClient().get_enphase_system_information(session)
        print(f"Summary: {summary}")
        print(f"Devices: {devices}")
        print(f"Sys Info: {sys_info}")


if __name__ == "__main__":
    asyncio.run(main())
