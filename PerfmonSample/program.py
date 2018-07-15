from sdspy import *
import configparser
import inspect


def get_app_settings(config_file):
    retval = {}
    e = xml.etree.ElementTree.parse(config_file)
    xml_settings = e.findall('./appSettings/add')
    for elem in xml_settings:
        k = elem.attrib['key']
        v = elem.attrib['value']
        retval[k] = v
    return retval

def isprop(v):
  return isinstance(v, property)

def toString(event):
    string = ""
    for k, v in event.__dict__.items():
        if k != 'typeId':
            if k == 'Time':
                string  = "{}: {}".format(v, string)
            elif v is None:
                string += "{}: , ".format(k)
            else:
                string += "{}: {}, ".format(k, v)
    return string[:-2]


def main():
    prg = Program()
    prg.run()


class Program:
    def __init__(self):
        # TODO: handle edge cases
        self.app_settings = get_app_settings('./app.config')
        self.views = []
        self.types = []
        self.streams = []

    # we'll use the following for cleanup, supressing errors
    @staticmethod
    def supress_error(sds_call):
        try:
            sds_call()
        except Exception as e:
            print(("Encountered Error: {error}".format(error=e)))

    def cleanup_single(self, client, namespace_id, type_id):
        print("Cleaning up")
        print("Deleting the stream")
        self.supress_error(lambda: client.deleteStream(namespace_id, type_id + 'Stream'))
        # print("Deleting the views")
        # self.supress_error(lambda: client.deleteView(namespace_id, view.Id))
        print("Deleting the types")
        self.supress_error(lambda: client.deleteType(namespace_id, type_id))

    def cleanup(self, client, namespace_id, views, types, streams):
        print("Cleaning up")
        print("Deleting the stream")
        for stream in streams:
            self.supress_error(lambda: client.deleteStream(namespace_id, stream.id))

        print("Deleting the views")
        for view in views:
            self.supress_error(lambda: client.deleteView(namespace_id, view.id))

        print("Deleting the types")
        for elem in types:
            self.supress_error(lambda: client.deleteType(namespace_id, elem.id))

    # Generate a new WaveData event
    def nextEvent(self, typeId):
        new_event = SdsTypeData(typeId)
        counters = PC().get_counters(typeId)

        for i, value in enumerate(counters):
            new_event.__setattr__(counters._fields[i], value)
        return new_event

    def run(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        client = SdsClient(config.get('Access', 'Tenant'), config.get('Access', 'Address'),
                           config.get('Credentials', 'Resource'),  config.get('Credentials', 'Authority'),
                           config.get('Credentials', 'Clientid'),  config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')
        print("------------------------------------------")
        print("  _________    .___     __________        ")
        print(" /   _____/  __| _/_____\______   \___.__.")
        print(" \_____  \  / __ |/  ___/|     ___<   |  |")
        print(" /        \/ /_/ |\___ \ |    |    \___  |")
        print("/_______  /\____ /____  >|____|    / ____|")
        print("        \/      \/    \/           \/     ")
        print("------------------------------------------")
        print("Sds endpoint at {}".format(client.Uri))
        print()

        # client = SdsClient(self.app_settings.get('tenantId'),
        #                    self.app_settings.get('address'),
        #                    self.app_settings.get('resource'),
        #                    self.app_settings.get('authority'),
        #                    self.app_settings.get('clientId'),
        #                    self.app_settings.get('clientSecret'),
        #                    namespace_id)
        ######################################################################################################
        # The following define the identifiers we'll use throughout
        ######################################################################################################

        # namespace_id = self.app_settings.get('namespaceId')
        # tenant_id = self.app_settings.get('tenantId')

        categories = ['Memory']
        # self.cleanup_single(client, namespaceId, 'Memory')
        for typeId in categories:
            #####################################################################
            # SdsType get or creattion
            #####################################################################
            print("Creating an Sds Type for '{}'".format(typeId))
            type = getCategoryDataType(typeId)
            type = client.getOrCreateType(namespaceId, type)
            # self.types.append(type) # uncomment or delete after testing

            #####################################################################
            # Sds Stream creation
            #####################################################################
            # TODO: each type isntance (e.g. multiple disks or processors) should each be on a unique stream
            print("Creating an Sds Stream for '{}'".format(typeId))
            print()
            stream = SdsStream(id="{}Stream".format(typeId), name="{}Stream".format(typeId),
                               description="A Stream to store '{}' events".format(typeId),
                               typeId=type.Id)

            client.createOrUpdateStream(namespaceId, stream)
            # self.streams.append(stream) # uncomment or delete after testing


            #####################################################################
            # CRUD operations for events
            #####################################################################
            start = datetime.datetime.now()
            span = datetime.datetime.strptime("0:1:0", "%H:%M:%S")

            # Insert a single event
            event = self.nextEvent(typeId)
            client.insertValue(namespaceId, stream.id, event)

            # Insert a list of events
            events = [self.nextEvent(typeId) for _ in range(2)]
            client.insertValues(namespaceId,stream.id,events)

            # Get the last event inserted in a stream
            print("Getting latest '{}' event".format(typeId))
            event = client.getLastValue(namespaceId, stream.id, SdsTypeData)
            print(toString(event))
            print()

            # Get all events
            events = client.getWindowValues(namespaceId, stream.id, SdsTypeData, str(start),
                                            end=str(datetime.datetime.utcnow()))

            print("Getting all '{}' events".format(typeId))
            print("Total '{}' events found: {}".format( typeId, str(len(events))))

            for i, event in enumerate(events):
                print("{}. {}".format(i+1, toString(event)))
            print()

            print("Updating events")
            # Update the first event
            # event = self.nextEvent(typeId)
            # client.updateValue(namespaceId, stream.id, event)

            # Update the rest of the events, adding events that have no prior index entry
            # updatedEvents = []
            # for i in range(2, 40, 2):
            #     event = self.nextEvent(typeId)
            #     updatedEvents.append(event)
            # client.updateValues(namespaceId, stream.id, updatedEvents)


            ######################################################################################################
            # SdsType, SdsStream, SdsView and SdsBehavior deletion
            ######################################################################################################
            # Cleanup the remaining artifacts
            self.cleanup_single(client, namespaceId, typeId)
            # self.cleanup(client, namespaceId, self.views, self.types, self.streams)


def get_events_in_window(client, stream_id, ret_obj, start, end, view_id=""):
    base_path = "/api/Tenants/{}/Namespaces/{}".format(client.tenantId, client.namespaceId)
    data_path = base_path + "/Streams/{}/Data".format(stream_id)
    url = client.url + data_path + "/GetWindowValues?startIndex={}&endIndex={}&viewId={}".format(start, end, view_id)
    req = RequestManager(client, url, "get")
    req.execute()
    content = json.loads(req.content)

    values = []
    for c in content:
        values.append(ret_obj.from_dictionary(c))

    return values


def get_last_event(client, stream, ret_obj, view_id=""):
    # get counters from stream
    base_path = "/api/Tenants/{}/Namespaces/{}".format(client.tenantId, client.namespaceId)
    data_path = base_path + "/Streams/{}/Data".format(stream.id)
    url = client.url + data_path + "/GetLastValue?viewId={}".format(view_id)
    req = RequestManager(client, url, "get")
    req.execute()
    content = json.loads(req.content)
    ret_obj = ret_obj.from_json(content)
    return ret_obj


def insert_counters(client, stream, counters, type_id):
    data = SdsTypeData(type_id)
    for i, value in enumerate(counters):
        data.__setattr__(counters._fields[i], value)
    req_url = "{}/api/Tenants/{}/Namespaces/{}/Streams/{}/Data/InsertValue".format(
        client.url, client.tenantId, client.namespaceId, stream.id)
    req = RequestManager(client, req_url, "post")
    req.payload = data.to_json()
    req.execute()


def getCategoryDataType(sample_type_id):
    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError('sample_type_id is not an instantiated string')

    category = SdsType()
    category.Id = sample_type_id
    category.Name = sample_type_id + "DataSample"
    category.Description = "This is a sample Sds type for storing {}Data events".format(sample_type_id)
    category.SdsTypeCode = SdsTypeCode.Object
    category.Properties = []

    int_type = SdsType()
    int_type.Id = 'intType'
    int_type.SdsTypeCode = SdsTypeCode.Int64

    double_type = SdsType()
    double_type.Id = 'doubleType'
    double_type.SdsTypeCode = SdsTypeCode.Double

    date_time_type = SdsType()
    date_time_type.Id = 'dateTimeType'
    date_time_type.SdsTypeCode = SdsTypeCode.DateTime

    string_type = SdsType()
    string_type.Id = 'stringType'
    string_type.SdsTypeCode = SdsTypeCode.String

    # time_prop is the primary key
    time_prop = SdsTypeProperty()
    time_prop.Id = 'Time'
    time_prop.SdsType = date_time_type
    time_prop.IsKey = True
    category.Properties.append(time_prop)

    type_id_prop = SdsTypeProperty()
    type_id_prop.Id = 'TypeId'
    type_id_prop.SdsType = string_type
    category.Properties.append(type_id_prop)

    # get and append counters to properties
    counters = PC().get_counters(sample_type_id)

    for field in counters._fields:
        prop = SdsTypeProperty()
        prop.Id = field
        prop.Name = field
        prop.SdsType = int_type
        category.Properties.append(prop)

    return category


if __name__ == "__main__":
    main()
