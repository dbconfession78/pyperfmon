import requests
import datetime
from program import *
import psutil


class SdsStream:
    def __init__(self, Id, Name, TypeId):
        self.Id = Id
        self.Name = Name
        self.TypeId = TypeId


stream = SdsStream(
    Id='<category name>--<instance name>',
    Name='<category name> <instance name>',
    TypeId='<type id>'
)

retval = '{'
retval += '   "Time":"{}"'.format(datetime.datetime.utcnow())
# for counter in counters: # TODO: build counters into json
retval += ','
retval += '"   "<counter name>": "raw value"'
retval += '}'

settings = get_app_settings()
base_address = "{}/api/Tenants/{}/Namespaces/{}".format(settings['address'], settings['tenant'], settings['namespace'])

r = requests.post('{}Streams/{}/Data/InsertValue'.format(base_address, stream.Id), data=retval)
print(r.status_code)
print()
