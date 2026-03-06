from dotenv import load_dotenv
import os
import aiohttp
load_dotenv()
syte_url = f"http://{os.getenv('syte_ip')}:5000"
import requests

session = requests.Session()

async def init_http():
    global session
    session = aiohttp.ClientSession()

async def close_http():
        await session.close()