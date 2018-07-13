from enum import Enum
# from SdsType import SdsType
import SdsType

class SdsTypeProperty(object):
    """Sds type property definition"""
    def __init__(self):
        self.__IsKey = False
        self.prop_names = ['Id', 'IsKey', 'name', 'description', 'SdsType', 'value', 'order']

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
    def description(self):
        return self.__description
    @description.setter
    def description(self, description):
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
    def value(self):
        return self.__value
    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def order(self):
        return self.__order
    @order.setter
    def order(self, order):
        self.__order = order

    def to_dictionary(self):
        dictionary = { 'IsKey': self.IsKey}

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'name'):
            dictionary['name'] = self.name

        if hasattr(self, 'description'):
            dictionary['description'] = self.description

        if hasattr(self, 'SdsType'):
            dictionary['SdsType'] = self.SdsType.to_dictionary()

        if hasattr(self, 'value'):
            if(isinstance(self.value, Enum)):
                dictionary['value'] = self.value.name
            else:
                dictionary['value'] = self.value

        if hasattr(self, 'order'):
            dictionary['order'] = self.order

        return dictionary

    def from_dictionary(self, content):
        type_property = SdsTypeProperty()

        if len(content) == 0:
            return type_property

        for prop_name in self.prop_names:
            if prop_name in content:
                if prop_name == 'SdsType':
                    val = SdsType.from_dictionary(content[prop_name])
                else:
                    val = content[prop_name]
                type_property.__setattr__(prop_name, val)

        return type_property