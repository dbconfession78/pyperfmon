import requests
import time
import datetime
import xml.etree.ElementTree
import xml
from performance_counters import PerformanceCounters as PC
from application_authentication_handler import ApplicationAuthenticationHandler
import json
from SdsClient import SdsClient
from SdsType import SdsType
from SdsTypeCode import SdsTypeCode
from SdsTypeProperty import SdsTypeProperty
from SdsStream import SdsStream


def get_app_settings(config_file):
    retval = {}
    e = xml.etree.ElementTree.parse(config_file)
    xml_settings = e.findall('./appSettings/add')
    for  elem in xml_settings:
        k = elem.attrib['key']
        v = elem.attrib['value']
        retval[k] = v
    return retval

def main():
    prg = Program()
    prg.run()

class Program:
    def __init__(self):
        # TODO: handle edge cases
        self.app_settings = get_app_settings('./app3.config')

    # we'll use the following for cleanup, supressing errors
    def supress_error(self, sdsCall):
        try:
            sdsCall()
        except Exception as e:
            print(("Encountered Error: {error}".format(error=e)))

    def cleanup(self, client, namespace_id):
        print("Cleaning up")
        print("Deleting the stream")
        self.supress_error(lambda: client.deleteStream(namespace_id, 'Memory'))

        # print("Deleting the views")
        # self.supress_error(lambda: client.deleteView(namespace_id, 'Memory_SampleView'))
        # self.supress_error(lambda: client.deleteView(namespace_id, sample_view_int_id))
        #
        # print("Deleting the types")
        # self.supress_error(lambda: client.deleteType(namespace_id, sample_type_id))
        # self.supress_error(lambda: client.deleteType(namespace_id, sample_target_type_id))
        # self.supress_error(lambda: client.deleteType(namespace_id, sample_Integer_Type_id))

    def run(self):
        sample_type_id = 'PerfmonData_SampleType'
        sample_target_type_id = 'PerfmonDataTarget_Sample_type'
        sample_Integer_Type_id = 'PerfmonData_IntegerType'
        sample_stream_id = 'PerfmonData_SampleStream'
        sample_stream_name = 'PerfmonPySample'
        sample_behavior_id = 'PerfmonData_SampleBehavior'
        sample_view_id = 'Perfmon_SampleView'
        sample_view_int_id = 'PerfmonData_SampleIntView'
        namespace_id = self.app_settings.get('namespaceId')

        # auth_handler = ApplicationAuthenticationHandler(self.app_settings)
        client = SdsClient(self.app_settings.get('tenantId'),
                           self.app_settings.get('address'),
                           self.app_settings.get('resource'),
                           self.app_settings.get('authority'),
                           self.app_settings.get('clientId'),
                           self.app_settings.get('clientSecret'))



        #TODO: DELETE OR COMMENT THIS AFTER TESTING
        # client.deleteType(self.app_settings.get('namespaceId'),'ProcessorStream')
        # client.deleteType(self.app_settings.get('namespaceId'),'MemoryStream')
        # self.cleanup(client, namespace_id)
        categories = ['Memory']

        for cat in categories:
            #####################################################################
            # SdsType get or create
            #####################################################################
            print("Creating an Sds Type for '{}'".format(cat))
            type = get_category_type(cat)
            type = client.get_or_create_type(self.app_settings.get('namespaceId'), type)

            #####################################################################
                # SdsStream creation
            #####################################################################
            print("Creating an Sds Stream for '{}'".format(cat))
            stream = SdsStream()
            stream.Id = "{}Stream".format(cat)
            stream.name = "{}Stream".format(cat)
            stream.description = "A Stream to store '{}' events".format(cat)
            stream.typeId = type.Id
            stream.behavior_id = None
            client.createOrUpdateStream(self.app_settings.get('namespaceId'), stream)

            #####################################################################
                # CRUD operations for events
            #####################################################################
            start = datetime.datetime.now()
            span = datetime.datetime.strptime("0:1:0", "%H:%M:%S")
            print("Inserting data")
            # Insert a single event
            # event
            # client.insertValue(self.app_settings.get('namespaceId'), stream.Id, )



def get_category_type(sample_type_id):
    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError('sample_type_id is not an instantiated string')

    category = SdsType()
    category.Id = sample_type_id
    category.name = sample_type_id + "DataSample"
    category.description = "This is a sample Sds type for storing {}Data events".format(sample_type_id)
    category.SdsTypeCode = SdsTypeCode.Object
    category.properties = []

    int_type = SdsType()
    int_type.Id = 'intType'
    int_type.SdsTypeCode = SdsTypeCode.Int64

    double_type = SdsType()
    double_type.Id = 'doubleType'
    double_type.SdsTypeCode = SdsTypeCode.Double

    date_time_type = SdsType()
    date_time_type.Id = 'dateTimeType'
    date_time_type.SdsTypeCode = SdsTypeCode.DateTime

    ### time_prop is the primary key ###
    time_prop = SdsTypeProperty()
    time_prop.Id = 'Time'
    time_prop.SdsType = date_time_type
    time_prop.IsKey = True
    category.properties.append(time_prop)

    ### get and append counters to properties
    counters = PC().get_counters(sample_type_id)
    # if type(counters) is list:
    #     for elem in counters:
    #         for field in elem._fields:
    #             prop = SdsTypeProperty()
    #             prop.Id = field
    #             prop.name = field
    #             prop.SdsType = int_type
    #             category.properties.append(prop)
    # else:
    for field in counters._fields:
        prop = SdsTypeProperty()
        prop.Id = field
        prop.name = field
        prop.SdsType = int_type
        category.properties.append(prop)

    return category


if __name__ == "__main__":
    main()