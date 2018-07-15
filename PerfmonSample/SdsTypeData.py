import json
import datetime
import time
import adal
import inspect
import psutil
from performance_counters import PerformanceCounters as PC

class SdsTypeData:
    def __init__(self, typeId=None):
        self.typeId = typeId
        self.time = None

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        if self.time is None:
            self.time = datetime.datetime.utcnow()
        dictionary = {'Time': str(self.time) }
        dictionary['Typeid'] = self.typeId
        for k, v in self.__dict__.items():
            if k != 'time':
                dictionary[k] = v
        self.__properties = dictionary
        return dictionary

    @staticmethod
    def from_json(json_obj):
        return SdsTypeData.from_dictionary(json_obj)

    @staticmethod
    def from_dictionary(content):
        if content is None:
            return SdsTypeData()
        typeId = content.get('TypeId')
        data_obj = SdsTypeData(typeId)
        prop_names = PC().get_counter_names(typeId)

        if len(content) == 0:
            return data_obj

        data_obj.__setattr__('Time', content['Time'])
        for prop in prop_names:
            # Pre-Assign the default
            data_obj.__setattr__(prop, 0)

            # If found in JSON object, then set
            if prop in content:
                value = content.get(prop)
                if value is not None:
                    data_obj.__setattr__(prop, value)
                    # prop.fset(data_obj, value)

        return data_obj