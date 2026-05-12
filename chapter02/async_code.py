# import time, random
#
#
# def process_task(item):
#     print("开始处理：", item)
#     # 假设一个任务的处理时间在0.5~2秒之间的一个随机数
#     process_time = random.uniform(0.5, 2.0)
#     time.sleep(process_time)
#     print(f"处理完成：{item}，耗时 {process_time:.2f} 秒")
#
#
# def process_all():
#     items = ["任务A", "任务B", "任务C", "任务D"]
#     for item in items:
#         process_task(item)
#
#
# if __name__ == "__main__":
#     start = time.time()
#     process_all()
#     end = time.time()
#     print(f"总耗时：{end - start:.2f} 秒")



import time, random, asyncio

async def process_task(item):
    print("开始处理：", item)
    # 假设一个任务的处理时间在0.5~2秒之间的一个随机数
    process_time = random.uniform(0.5, 2.0)
    await asyncio.sleep(process_time)
    print(f"处理完成：{item}，耗时 {process_time:.2f} 秒")


async def process_all():
    items = ["任务A", "任务B", "任务C", "任务D"]
    tasks = [asyncio.create_task(process_task(item)) for item in items]
    await asyncio.gather(*tasks)

async def main():
    start = time.time()
    await process_all()
    end = time.time()
    print(f"总耗时：{end - start:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())