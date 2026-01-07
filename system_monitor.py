import psutil
import time
from aiohttp import web
from server import PromptServer

# Global state for calculating Disk Write Rate
last_disk_write = 0
last_time = time.time()
first_run = True

async def get_system_stats(request):
    global last_disk_write, last_time, first_run

    # 1. Get Swap Memory
    swap = psutil.swap_memory()
    
    # 2. Get Disk I/O
    try:
        disk = psutil.disk_io_counters()
        current_disk_write = disk.write_bytes
    except:
        current_disk_write = 0

    current_time = time.time()
    time_delta = current_time - last_time

    # Avoid division by zero
    if time_delta <= 0:
        time_delta = 0.001

    # Calculate Speed (Bytes per second)
    if first_run:
        write_rate = 0
        first_run = False
    else:
        write_rate = (current_disk_write - last_disk_write) / time_delta

    # Convert to MB
    write_rate_mb = write_rate / (1024 * 1024)
    
    # Update globals for next tick
    last_disk_write = current_disk_write
    last_time = current_time

    return web.json_response({
        "swap_percent": swap.percent,
        "swap_used_gb": round(swap.used / (1024**3), 2),
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "disk_write_mb": round(write_rate_mb, 2)
    })

# Register the API route in ComfyUI
# This allows the JS to call /api/swap_monitor/stats
try:
    PromptServer.instance.app.router.add_get('/api/swap_monitor/stats', get_system_stats)
except Exception as e:
    print(f"Error registering Monitor API: {e}")