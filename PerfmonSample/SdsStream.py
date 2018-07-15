import json
from SdsStreamIndex import SdsStreamIndex


class SdsStream(object):
    """Sds stream definition"""
    def __init__(self, id, name, typeId, description):
        self.id = id
        self.name = name
        self.__typeId = typeId
        self.__description = description

    @property
    def id(self):
        return self.__Id

    @id.setter
    def id(self, Id):
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
    def TypeId(self):
        return self.__typeId

    @TypeId.setter
    def TypeId(self, typeId):
        self.__typeId = typeId

    @property
    def BehaviorId(self):
        return self.__behavior_id

    @BehaviorId.setter
    def BehaviorId(self, behavior_id):
        self.__behavior_id = behavior_id

    @property
    def Indexes(self):
        return self.__indexes

    @Indexes.setter
    def Indexes(self, indexes):
        self.__indexes = indexes

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'Id': self.id, 'TypeId': self.TypeId}

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'BehaviorId'):
            dictionary['BehaviorId'] = self.BehaviorId

        if hasattr(self, 'Indexes'):
            dictionary['Indexes'] = []
            for value in self.Indexes:
                dictionary['Indexes'].append(value.to_dictionary())

        return dictionary

    @staticmethod
    def from_json(jsonObj):
        return SdsStream.from_dictionary(jsonObj)

    @staticmethod
    def from_dictionary(content):
        stream = SdsStream()

        if len(content) == 0:
            return stream

        if 'Id' in content:
            stream.id = content['Id']

        if 'Name' in content:
            stream.Name = content['Name']

        if 'Description' in content:
            stream.Description = content['Description']

        if 'TypeId' in content:
            stream.TypeId = content['TypeId']

        if 'BehaviorId' in content:
            stream.BehaviorId = content['BehaviorId']

        if 'Indexes' in content:
            indexes = content['Indexes']
            if indexes is not None and len(indexes) > 0:
                stream.Indexes = []
                for value in indexes:
                    stream.Indexes.append(SdsStreamIndex.from_dictionary(value))

        return stream
