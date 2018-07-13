# from JsonEncoder import Encoder
import json
import inspect
from SdsViewProperty import SdsViewProperty


class SdsView(object):
    """Sds view definitions"""

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
    def sourceTypeId(self):
        return self.__sourceTypeId

    @sourceTypeId.setter
    def sourceTypeId(self, base_type):
        self.__sourceTypeId = base_type

    @property
    def targetTypeId(self):
        return self.__targetTypeid

    @targetTypeId.setter
    def targetTypeId(self, type_code):
        self.__targetTypeId = type_code

    @property
    def properties(self):
        return self.__properties

    @properties.setter
    def properties(self, properties):
        self.__properties = properties

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'id': self.Id, 'source_type_id': self.source_type_id, 'target_type_id': self.target_type_id}

        # optional properties
        if hasattr(self, 'properties'):
            dictionary['properties'] = []
            for value in self.properties:
                dictionary['properties'].append(value.to_dictionary())

        if hasattr(self, 'name'):
            dictionary['name'] = self.name

        if hasattr(self, 'description'):
            dictionary['description'] = self.description

        return dictionary

    @staticmethod
    def from_json(json_obj):
        return SdsView.from_dictionary(json_obj)

    @staticmethod
    def from_dictionary(content):
        view = SdsView()
        prop_names = ['id', 'IsKey', 'name', 'description', 'SdsType', 'value', 'order']

        if len(content) == 0:
            return view
        for prop_name in prop_names:
            if prop_name in content:
                if prop_name == 'properties':
                    prop_val = []
                    properties = content.get('properties')
                    if properties and len(properties) > 0:
                        for prop in properties:
                            prop_val.append(SdsViewProperty.from_dictionary(prop))
                else:
                    prop_val = content[prop_name]
                view.__setattr__(prop_name, prop_val)

        # if 'id' in content:
        #     view.id = content['id']
        #
        # if 'name' in content:
        #     view.Name = content['name']
        #
        # if 'description' in content:
        #     view.description = content['description']
        #
        # if 'target_type_id' in content:
        #     view.target_type_id = content['target_type_id']
        #
        # if 'source_type_id' in content:
        #     view.source_type_id = content['source_type_id']

        # if 'properties' in content:
        #     properties = content['properties']
        #     if properties is not None and len(properties) > 0:
        #         view.properties = []
        #         for prop in properties:
        #             view.properties.append(SdsViewProperty.from_dictionary(prop))

        return view