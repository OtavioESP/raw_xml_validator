import re
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

    def _validate_data_type(self, referred_type: str, data: str) -> bool:
        '''
        Validate if the referred data type in xsd is right or not
        '''
        if referred_type == 'xs:byte':
            try:
                int_value = int(data)
                return True
            except ValueError:
                return False

        elif referred_type == 'xs:float':
            try:
                float(data)
                return True
            except ValueError:
                return False

        elif referred_type == 'xs:string':
            if isinstance(data, str):
                if re.fullmatch(r'^-?\d+(\.\d+)?$', data):
                    return False
                else:
                    return True

        else:
            return False


    def _validate_depth(self, depth: int, tag_name: str) -> None:
        if not depth == self.XSD_DATA[tag_name]['profundidade']:
            raise ValueError(f'A tag {tag_name} não possui uma a mesma profundidade do que o XSD.')


    def _validate_by_xsd(self, tags: list) -> bool:

        depth_counter = 0
        validation_dict = {}
        tag_name = ''

        for key, value in enumerate(tags):

            if self._identify_value(value) == self._TagType.OPEN:
                tag_name = self._clear_tag(value)
                self._validate_depth(depth_counter, tag_name)
                validation_dict[tag_name] = dict(profundidade=depth_counter)
                depth_counter += 1

            if self._identify_value(value) == self._TagType.CLOSE:
                tag_name = self._clear_tag(value)
                depth_counter -= 1
                self._validate_depth(depth_counter, tag_name)
                validation_dict[tag_name] = dict(profundidade=depth_counter)

            if self._identify_value(value) == self._TagType.NOT_A_TAG:
                xsd_tag_type = self.XSD_DATA[tag_name]['tipo']

                if self._validate_data_type(xsd_tag_type, value):
                    continue
                else:
                    raise ValueError(f'A Tag {tag_name} não possui um tipo de dado {xsd_tag_type}')

        for key in self.XSD_DATA:
            if key not in validation_dict:
                raise ValueError(f'Tag {key} não existente no XML')

        return True

    def read_file(self) -> list:
        tag_list = []
        lines = open(self.FILE_PATH, 'r').readlines()
        for l in lines:
            sanitized_tag = self._sanitize_tag(l)
            tag_list.append(sanitized_tag)

        return tag_list

    def run(self) -> bool:
        tags = self.read_file()
        try:
            self._validate_by_xsd(tags)
            print(15*'=-=')
            print('VALIDATED !!!')
            print(15*'=-=')
            return True

        except ValueError as exc:
            print(exc)
            return False

        except KeyError as exc:
            print(f'A tag {exc} não foi compreendida pelo XSD.')
            return False
