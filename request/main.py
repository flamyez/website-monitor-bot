import aiohttp

async def chk_website(url):
    try:
        print(f"[REQUESTS] Checking URL {url}.")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                if response.status == 200:
                    return True
                else:
                    return False
    except Exception:
        return False