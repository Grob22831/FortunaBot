from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()

syte_url = f"http://{os.getenv('syte_ip')}:5000"

session: aiohttp.ClientSession | None = None


async def init_http():
    global session
    session = aiohttp.ClientSession()


async def close_http():
    global session
    if session:
        await session.close()