import sys
import inspect
import asyncio
from subprocess import PIPE


async def run_sleep():
    proc = await asyncio.create_subprocess_exec(
        "sleep",
        "0.002",
        stdout=PIPE,
    )
    await proc.communicate()


async def amain():
    loop = asyncio.get_running_loop()
    task = asyncio.current_task(loop)
    coro = task.get_coro()

    called_cancel = False

    def cancel_eventually():
        my_coro = coro
        while inspect.iscoroutine(my_coro.cr_await):
            my_coro = my_coro.cr_await
        if my_coro.cr_code is loop._make_subprocess_transport.__code__:
            print("_cancel_all_tasks")
            tasks = asyncio.all_tasks()
            for task in tasks:
                task.cancel()
        else:
            loop.call_soon(cancel_eventually)

    loop.call_soon(cancel_eventually)
    await run_sleep()


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    sys.exit(main())
