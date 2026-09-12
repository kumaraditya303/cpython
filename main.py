import mmap, gc, sys, threading, queue, time, tracemalloc, ctypes, os, subprocess

if sys.platform == "darwin":
    libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
    libc.malloc_zone_pressure_relief.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    libc.malloc_zone_pressure_relief.restype = ctypes.c_size_t
    def _trim():
        libc.malloc_zone_pressure_relief(None, 0)
    def _rss_kb():
        out = subprocess.check_output(["ps", "-o", "rss=", "-p", str(os.getpid())])
        return int(out)
else:
    libc = ctypes.CDLL("libc.so.6")
    def _trim():
        libc.malloc_trim(0)
    def _rss_kb():
        with open('/proc/self/status') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    return int(line.split()[1])

def rss_mb():
    _trim()
    return _rss_kb() // 1024

# FT object header: ob_tid(8) ob_flags(2) ob_mutex(1) ob_gc_bits(1) ob_ref_local(4) ob_ref_shared(8)
def ref_shared(addr):
    return ctypes.c_ssize_t.from_address(addr + 16).value
def ref_local(addr):
    return ctypes.c_uint32.from_address(addr + 12).value

N = 500
SIZE = 1024 * 1024
MODE = sys.argv[1] if len(sys.argv) > 1 else "blocked"

gc.disable()
q = queue.Queue()
a_done = threading.Event()
release_a = threading.Event()
addrs = []

def owner():
    for i in range(N):
        obj = mmap.mmap(-1, SIZE); obj[:] = b"x" * SIZE
        addrs.append(id(obj))
        q.put(obj)
        del obj
    a_done.set()
    if MODE == "blocked":
        release_a.wait()               # detached in lock acquire
    elif MODE == "spin":
        while not release_a.is_set():  # runs bytecode -> eval breaker drains queue
            pass

def consumer():
    a_done.wait()
    for i in range(N):
        obj = q.get()
        del obj

tracemalloc.start()
ta = threading.Thread(target=owner); tb = threading.Thread(target=consumer)
ta.start(); tb.start(); tb.join()
time.sleep(0.3)
cur, _ = tracemalloc.get_traced_memory()
print(f"[{MODE}] after B dropped refs: RSS={rss_mb()} MB traced={cur//2**20} MB")
if MODE == "blocked":
    # object still alive; low 2 bits of ob_ref_shared == 2 means _Py_REF_QUEUED
    a = addrs[0]
    print(f"  obj0 ob_ref_local={ref_local(a)} ob_ref_shared=0x{ref_shared(a):x} (QUEUED flag={ref_shared(a) & 3 == 2})")
    gc.collect()
    cur, _ = tracemalloc.get_traced_memory()
    print(f"  after gc.collect(): RSS={rss_mb()} MB traced={cur//2**20} MB")
release_a.set(); ta.join()