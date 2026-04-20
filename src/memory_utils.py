import psutil


BYTES_PER_COLUMN = 300
BYTES_PER_ROW_OVERHEAD = 200
MAX_BATCH_SIZE = 1000000
MIN_BATCH_SIZE = 5000


def get_available_memory_mb():
    return psutil.virtual_memory().available / (1024 * 1024)


def calculate_batch_size(num_columns: int, memory_percentage: float = 5.0) -> int:
    available_mb = get_available_memory_mb()
    bytes_per_row = BYTES_PER_ROW_OVERHEAD + (num_columns * BYTES_PER_COLUMN)
    bytes_available = (available_mb * 1024 * 1024) * (memory_percentage / 100)
    batch_size = int(bytes_available / bytes_per_row)
    return max(MIN_BATCH_SIZE, min(MAX_BATCH_SIZE, batch_size))


def get_system_info():
    mem = psutil.virtual_memory()
    return {
        "total_memory_mb": mem.total / (1024 * 1024),
        "available_memory_mb": mem.available / (1024 * 1024),
        "memory_percent_used": mem.percent,
        "suggested_batch_size": calculate_batch_size(num_columns=10)
    }