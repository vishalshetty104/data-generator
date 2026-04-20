import psutil


def get_available_memory_mb():
    return psutil.virtual_memory().available / (1024 * 1024)


def calculate_batch_size():
    available_mb = get_available_memory_mb()
    if available_mb > 8000:
        return 100000
    elif available_mb > 4000:
        return 50000
    else:
        return 10000


def get_system_info():
    mem = psutil.virtual_memory()
    return {
        "total_memory_mb": mem.total / (1024 * 1024),
        "available_memory_mb": mem.available / (1024 * 1024),
        "memory_percent_used": mem.percent,
        "suggested_batch_size": calculate_batch_size()
    }