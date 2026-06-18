import asyncio, time

async def fetch_url(site_name, delay):
    print(f"start loading site - {site_name}")
    await asyncio.sleep(delay)
    print(f"{site_name} loaded for {delay} sec")
    return f"Data {site_name}"

async def main():
    start_time = time.time()
    list_tasks = [
        fetch_url(site_name = "google", delay = 2),
        fetch_url(site_name = "github", delay = 3),
        fetch_url(site_name = "moyo", delay = 1)
    ]
    results = await asyncio.gather(*list_tasks)
    end_time = time.time()
    print(f"all time: {end_time - start_time}")
    print(f"data was back: {results}")

asyncio.run(main())