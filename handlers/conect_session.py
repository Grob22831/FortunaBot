from dotenv import load_dotenv
import os
import aiohttp
import asyncio
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

async def get_session():
    global session
    while session is None:
        await asyncio.sleep(0.1)
    return session