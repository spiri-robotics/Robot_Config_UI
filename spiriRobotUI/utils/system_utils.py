import psutil

cores = psutil.cpu_count(logical=True)
# Total memory in GB
memory = round(psutil.virtual_memory().total / (1024 ** 3), 2)
# Total disk space in GB (for '/')
disk = round(psutil.disk_usage('/').total / (1024 ** 3), 2)