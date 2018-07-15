import psutil
class PerformanceCounters:
    def __init__(self):
        self.type_dct = {
            "Processor": psutil.cpu_times(),
            "Memory": psutil.virtual_memory(),
            "disks": psutil.disk_partitions(),
            "network": psutil.net_io_counters(pernic=True),
            #"sensors": psutil.sensors_temperatures(),
            "users": psutil.users(),
            "process management": psutil.pids()
        }

    def get_counters(self, cat_name):
        return self.type_dct[cat_name]
        # return self.type_dct[cat_name.lower()]

    def get_counter_names(self, cat_name):
        #TODO handle categories that don't have _fields (e.g. disks)
        return self.type_dct.get(cat_name)._fields