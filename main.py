#import threading
import asyncio
from crawler import crawler
async def get_data_from_crawler():
    my_crawler = crawler('YOUR LINK HERE')
    async for data in my_crawler.crawler():
        print(data)


if __name__ == '__main__':
    asyncio.run(get_data_from_crawler())

