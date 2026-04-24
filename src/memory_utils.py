import psutil

"""Memory utilities for batch size calculation and system information."""

BYTES_PER_COLUMN = 300
"""Estimated bytes per column for memory calculation."""

BYTES_PER_ROW_OVERHEAD = 200
"""Fixed overhead bytes per row for memory calculation."""

MAX_BATCH_SIZE = 1000000
"""Maximum allowed batch size."""

MIN_BATCH_SIZE = 5000
"""Minimum allowed batch size."""


def get_available_memory_mb():
    """Get available system memory in megabytes.

    Returns:
        Available memory in MB.
    """


def calculate_batch_size(num_columns: int, memory_percentage: float = 5.0) -> int:
    """Calculate appropriate batch size based on available memory.

    Args:
        num_columns: Number of columns in the data schema.
        memory_percentage: Percentage of available memory to use.

    Returns:
        Recommended batch size clamped between MIN and MAX batch size.
    """


def get_system_info():
    """Get system memory information and suggested batch size.

    Returns:
        Dictionary with total_memory_mb, available_memory_mb,
        memory_percent_used, and suggested_batch_size.
    """
    mem = psutil.virtual_memory()
    return {
        "total_memory_mb": mem.total / (1024 * 1024),
        "available_memory_mb": mem.available / (1024 * 1024),
        "memory_percent_used": mem.percent,
        "suggested_batch_size": calculate_batch_size(num_columns=10)
    }