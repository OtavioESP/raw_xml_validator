from typing import Any

class ValidateXML:
    '''
    This class validates a XML based on the data from a given XSD
    The data stands for this: {tag_name: {profundidade: int, tipo: string, valor: int | string | None}...}
    '''
    class _TagType:
        OPEN = 1
        CLOSE = 2
        NOT_A_TAG = 3

    def __init__(self, xsd_data: dict):
        self.XSD_DATA = xsd_data
        self.FILE_PATH = "./teste.xml"

    def _sanitize_tag(self, tag: str) -> str:
        return tag.strip("\n").strip(" ")

    def _clear_tag(self, tag: str) -> str:
        return tag.strip("</").strip("<").strip(">")

    def _identify_value(self, value: str) -> int:
        '''
        Returns if a given value is a tag or data
        '''
        if all(["<" in value, ">" in value, not "</" in value]):
            return self._TagType.OPEN

        if all(["</" in value, ">" in value]):
            return self._TagType.CLOSE

        return self._TagType.NOT_A_TAG

    def _validate_data_type(self, referred_type: str, data: Any) -> bool:
        '''
        Validate if the referred data type in xsd is right or not
        '''
        try:
            if  referred_type == ' xs: byte':
                int(data)
            if  referred_type == ' xs: float':
                float(data)

            return True
        except ValueError:
            return False


    def _validate_by_xsd(self, tags: list) -> bool:

        depth_counter = 0
        validation_dict = {}
        tag_name = ''

        for key, value in enumerate(tags):


            if self._identify_value(value) == self._TagType.OPEN:
                tag_name = self._clear_tag(value)
                validation_dict[tag_name] = dict(profundidade=depth_counter)
                depth_counter += 1

            if self._identify_value(value) == self._TagType.CLOSE:
                tag_name = self._clear_tag(value)
                depth_counter -= 1
                validation_dict[tag_name] = dict(profundidade=depth_counter)

            if self._identify_value(value) == self._TagType.NOT_A_TAG:
                if not self._validate_data_type(self.XSD_DATA[tag_name]['tipo'], value):
                    return False

            # TODO: VALIDACAO FINAL

        return True

    def read_file(self) -> list:
        tag_list = []
        lines = open(self.FILE_PATH, 'r').readlines()
        for l in lines:
            sanitized_tag = self._sanitize_tag(l)
            tag_list.append(sanitized_tag)

        return tag_list


    def run(self):
        tags = self.read_file()

        if self._validate_by_xsd(tags):
            print(15*'=-=')
            print('VALIDATED !!!')
            print(15*'=-=')
        else:
            print('INVALID XML FILE !')

        return
