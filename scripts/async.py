import asyncio
from random import random

# Define an asynchronous function (an awaitable)
async def my_awaitable_function(i=1):
    print(f"Function started, waiting for 1 second... [{i}]")
    await asyncio.sleep(1 + 2 * random())  # Yields control to the event loop
    print(f"Function finished. [{i}]")
    return f"Result Value [{i}]"


async def test():
    task_run = []
    for i in range(10):
        task_run.append(my_awaitable_function(i))

    return await asyncio.gather(*task_run)


# The main entry point of your program (a synchronous context)
if __name__ == "__main__":
    # Use asyncio.run() to execute the async function and manage the event loop
    # result = asyncio.run(my_awaitable_function())
    result = asyncio.run(test())
    # print(f"The returned result is")
    # result = my_awaitable_function()
    print(f"The returned result is: {result}")
