from enum import Enum
import SdsType

class SdsTypeProperty(object):
    """Sds type property definition"""
    def __init__(self):
        self.__IsKey = False

    @property
    def Id(self):
        return self.__Id
    @Id.setter
    def Id(self, Id):
        self.__Id = Id

    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, name):
        self.__name = name

    @property
    def Description(self):
        return self.__description
    @Description.setter
    def Description(self, description):
        self.__description = description

    @property
    def IsKey(self):
        return self.__IsKey
    @IsKey.setter
    def IsKey(self, IsKey):
        self.__IsKey = IsKey

    @property
    def SdsType(self):
        return self.__SdsType
    @SdsType.setter
    def SdsType(self, SdsType):
        self.__SdsType = SdsType

    @property
    def Value(self):
        return self.__value
    @Value.setter
    def Value(self, value):
        self.__value = value

    @property
    def Order(self):
        return self.__order
    @Order.setter
    def Order(self, order):
        self.__order = order

    def to_dictionary(self):
        dictionary = { 'IsKey': self.IsKey}

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'SdsType'):
            dictionary['SdsType'] = self.SdsType.to_dictionary()

        if hasattr(self, 'Value'):
            if(isinstance(self.Value, Enum)):
                dictionary['Value'] = self.Value.name
            else:
                dictionary['Value'] = self.Value

        if hasattr(self, 'Order'):
            dictionary['Order'] = self.Order

        return dictionary


    # @staticmethod
    # def from_dictionary_BAK(content):
    #     typeProperty = SdsTypeProperty()
    #
    #     if len(content) == 0:
    #         return typeProperty
    #
    #     if 'Id' in content:
    #         typeProperty.Id = content['Id']
    #
    #     if 'IsKey' in content:
    #         typeProperty.IsKey = content['IsKey']
    #
    #     if 'Name' in content:
    #         typeProperty.Name = content['Name']
    #
    #     if 'Description' in content:
    #         typeProperty.Description = content['Description']
    #
    #     if 'SdsType' in content:
    #         typeProperty.SdsType = SdsType.SdsType.from_dictionary(content['SdsType'])
    #
    #     if 'Value' in content:
    #         typeProperty.Value = content['Value']
    #
    #     if 'Order' in content:
    #         typeProperty.Order = content['Order']
    #
    #     return typeProperty

    @staticmethod
    def from_dictionary(content):
        prop_names = ['Id', 'IsKey', 'Name', 'Description', 'SdsType', 'Value', 'Order']
        typeProperty = SdsTypeProperty()

        if len(content) == 0:
            return typeProperty

        for prop_name in prop_names:
            if prop_name in content:
                if prop_name == 'SdsType':
                    val = SdsType.SdsType.from_dictionary(content['SdsType'])
                else:
                    val = content[prop_name]
                typeProperty.__setattr__(prop_name, val)

        return typeProperty