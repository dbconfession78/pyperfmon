from SdsTypeCode import SdsTypeCode
from SdsTypeProperty import SdsTypeProperty
import json
class SdsType(object):
    def __init__(self):
        self.SdsTypeCode = SdsTypeCode.Empty

    @property
    def Id(self):
        return self.__Id
    @Id.setter
    def Id(self, Id):
        self.__Id = Id

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def properties(self):
        return self.__properties
    @properties.setter
    def properties(self, properties):
        self.__properties = properties

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def base_type(self):
        return self.__base_type
    @base_type.setter
    def base_type(self, base_type):
        self.__base_type = base_type

    @property
    def SdsTypeCode(self):
        return self.__type_code
    @SdsTypeCode.setter
    def SdsTypeCode(self, type_code):
        self.__type_code = type_code

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        dictionary = {'SdsTypeCode': self.SdsTypeCode.value}

        if hasattr(self, 'properties'):
            dictionary['properties'] = []
            for prop in self.properties:
                dictionary['properties'].append(prop.to_dictionary())

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'name'):
            dictionary['name'] = self.name

        if hasattr(self, 'description'):
            dictionary['description'] = self.description

        if hasattr(self, 'base_type'):
            dictionary['base_type'] = self.base_type.to_dictionary()

        return dictionary

    @staticmethod
    def from_json(json_obj):
        return SdsType.from_dictionary(json_obj)

    @staticmethod
    def from_dictionary(content):
        type = SdsType()

        if len(content) == 0:
            return type

        if 'Id' in content:
            type.Id = content['Id']

        if 'name' in content:
            type.name = content['name']

        if 'description' in content:
            type.description = content['description']

        if 'SdsTypeCode' in content:
            type.SdsTypeCode = SdsTypeCode(content['SdsTypeCode'])

        if 'base_type' in content:
            type.base_type = SdsType.from_dictionary(content['base_type'])

        if 'properties' in content:
            properties = content['properties']
            if properties is not None and len(properties) > 0:
                type.properties = []
                for prop in properties:
                    type.properties.append(SdsTypeProperty.from_dictionary(prop))
        return type





