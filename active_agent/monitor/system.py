import psutil

def get_memory_usage():
    """
    Checks the system's memory usage and returns a dictionary with relevant details.
    """
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "available_gb": round(mem.available / (1024 ** 3), 2),
        "percent_used": mem.percent
    }

if __name__ == "__main__":
    print(f"Memory Usage: {get_memory_usage()}")
