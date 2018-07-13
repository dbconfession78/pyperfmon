import json
import SdsView


class SdsViewProperty(object):
    """Sds View Property definition"""

    @property
    def source_id(self):
        return self.__source_id

    @source_id.setter
    def source_id(self, id):
        self.__source_id = id

    @property
    def target_id(self):
        return self.__target_id

    @target_id.setter
    def target_id(self, name):
        self.__target_id = name

    @property
    def sds_view(self):
        return self.__sds_view

    @sds_view.setter
    def sds_view(self, description):
        self.__sds_view = description

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'source_id': self.source_id, 'target_id': self.target_id}

        if hasattr(self, 'sds_view'):
            dictionary['sds_view'] = self.sds_view.to_dictionary()

        return dictionary

    @staticmethod
    def from_json(json_obj):
        return SdsViewProperty.from_dictionary(json_obj)

    @staticmethod
    def from_dictionary(content):
        view_property = SdsViewProperty()

        if len(content) == 0:
            return view_property

        if 'source_id' in content:
            view_property.source_id = content['source_id']

        if 'target_id' in content:
            view_property.target_id = content['target_id']

        if 'sds_view' in content:
            view_property.SdsView = SdsView.from_dictionary(content['sds_view'])

        return view_property

