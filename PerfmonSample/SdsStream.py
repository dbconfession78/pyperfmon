import json
from SdsStreamIndex import SdsStreamIndex


class SdsStream(object):
    """Sds stream definition"""

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
    def typeId(self):
        return self.__typeId

    @typeId.setter
    def typeId(self, typeId):
        self.__typeId = typeId

    @property
    def behavior_id(self):
        return self.__behavior_id

    @behavior_id.setter
    def behavior_id(self, behavior_id):
        self.__behavior_id = behavior_id

    @property
    def indexes(self):
        return self.__indexes

    @indexes.setter
    def indexes(self, indexes):
        self.__indexes = indexes

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'id': self.Id, 'typeId': self.typeId}

        # optional properties
        if hasattr(self, 'name'):
            dictionary['name'] = self.name

        if hasattr(self, 'description'):
            dictionary['description'] = self.description

        if hasattr(self, 'behavior_id'):
            dictionary['behavior_id'] = self.behavior_id

        if hasattr(self, 'indexes'):
            dictionary['indexes'] = []
            for value in self.indexes:
                dictionary['indexes'].append(value.to_dictionary())

        return dictionary

    @staticmethod
    def from_json(jsonObj):
        return SdsStream.from_dictionary(jsonObj)

    @staticmethod
    def from_dictionary(content):
        stream = SdsStream()

        if len(content) == 0:
            return stream

        if 'id' in content:
            stream.Id = content['id']

        if 'name' in content:
            stream.name = content['name']

        if 'description' in content:
            stream.description = content['description']

        if 'typeId' in content:
            stream.typeId = content['typeId']

        if 'behavior_id' in content:
            stream.behavior_id = content['behavior_id']

        if 'indexes' in content:
            indexes = content['indexes']
            if indexes is not None and len(indexes) > 0:
                stream.indexes = []
                for value in indexes:
                    stream.indexes.append(SdsStreamIndex.from_dictionary(value))

        return stream

