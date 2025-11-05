import os
import subprocess

original_Popen_kill = subprocess.Popen.kill

def mocked_kill(self):
    print(f"mocked_kill called for pid {self.pid}")
    original_Popen_kill(self)

subprocess.Popen.kill = mocked_kill

from asyncio import Task, create_subprocess_exec, run, sleep
async def main():
    t = Task(create_subprocess_exec('sleep', '100'))
    await sleep(1)
    t.cancel()
    await t
run(main())