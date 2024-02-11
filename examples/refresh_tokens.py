import aiohttp
import asyncio

from enphase_home_api_client.enphase import EnphaseAPIClient


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        access_token, refresh_token = await EnphaseAPIClient().generate_new_enphase_tokens(session)
        print(f"ACCESS_TOKEN: {access_token}")
        print(f"REFRESH_TOKEN: {refresh_token}")


if __name__ == "__main__":
    asyncio.run(main())
