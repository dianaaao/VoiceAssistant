# import time

# start_time = time.time()
# def serve_table(table_num: int,):
#     print(f"waiter o n table num - {table_num}")
#     print(f"waiter take a order - {table_num}")
#     print(f"waiter goes to cooker and start cooking - {table_num}")
#     time.sleep(3)
#     print(f"meat for table {table_num} done")
#     print(f"waiter bring to table {table_num} the meat")

# for i in range(2):
#     serve_table(i)

# end_time = time.time()
# print(end_time - start_time)






import asyncio, time

async def cook_steak(table_num: int,):
    print(f"cooker start cooking meat for table - {table_num}")
    await asyncio.sleep(3)
    print(f"steak for table - {table_num} done")
    return f"steak for table - {table_num}"

async def serve_table(table_num: int,):
    print(f"waiter o n table num - {table_num}")
    print(f"waiter take a order - {table_num}")
    print(f"waiter goes to cooker and start cooking - {table_num}")

    steak_task = asyncio.create_task(cook_steak(table_num))
    steak = await steak_task
    print(f"waiter bring to table {table_num} the {steak}")

async def main():
    start_time = time.time()
    list_tasks = [
        asyncio.create_task(serve_table(1)),
        asyncio.create_task(serve_table(2)),
        asyncio.create_task(serve_table(3)),
    ]
    await asyncio.gather(*list_tasks)
    end_time = time.time()
    print(f"all time: {end_time - start_time}")

asyncio.run(main())