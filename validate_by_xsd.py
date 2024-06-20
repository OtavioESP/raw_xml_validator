import re

class ValidateByXSD:
    def __init__(self, xsd_file_path: str, xml_file_path: str):
        self.XSD_FILE_PATH = xsd_file_path
        self.XML_FILE_PATH = xml_file_path

    def read_file(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def extract_xsd_info(self, xsd_content: str):
        xsd_data = {}
        element_re = re.compile(r'<xs:element\s+([^>]+)>')
        name_re = re.compile(r'name="([^"]+)"')
        type_re = re.compile(r'type="([^"]+)"')
        max_occurs_re = re.compile(r'maxOccurs="([^"]+)"')
        min_occurs_re = re.compile(r'minOccurs="([^"]+)"')
        complex_type_re = re.compile(r'<xs:complexType>')

        for match in element_re.finditer(xsd_content):
            element_str = match.group(1)

            name_match = name_re.search(element_str)
            type_match = type_re.search(element_str)
            max_occurs_match = max_occurs_re.search(element_str)
            min_occurs_match = min_occurs_re.search(element_str)

            name = name_match.group(1) if name_match else None
            element_type = type_match.group(1) if type_match else ('complex' if complex_type_re.search(xsd_content[match.end():]) else None)
            max_occurs = max_occurs_match.group(1) if max_occurs_match else '1'
            min_occurs = min_occurs_match.group(1) if min_occurs_match else '0'

            xsd_data[name] = {
                'type': element_type,
                'max_occurs': max_occurs,
                'min_occurs': min_occurs,
            }

        return xsd_data

    def validate_type(self, element_content, expected_type):
        if expected_type == 'xs:string':
            return isinstance(element_content, str)
        return True

    # def validate_occurrences(self, parent_content, tag, min_occurs, max_occurs):
    #     if max_occurs == 'unbounded':
    #         return True  # No need to validate if occurrences are unbounded

    #     count = len(re.findall(f'<{tag}[^>]*>', parent_content))
    #     max_occurs = int(max_occurs)
    #     min_occurs = int(min_occurs)

    #     if min_occurs == 0 and count == 0:
    #         return True  # No need to check if minOccurs is 0 and count is 0

    #     # breakpoint()
    #     return min_occurs <= count <= max_occurs

    def extract_element_content(self, xml_content, tag):
        pattern = re.compile(f'<{tag}[^>]*>(.*?)</{tag}>', re.DOTALL)
        return pattern.findall(xml_content)

    def validate_xml(self, xml_content, xsd_data, parent_tag=None):
        for tag, data in xsd_data.items():
            tag_content_list = self.extract_element_content(xml_content, tag)
            # if not self.validate_occurrences(xml_content, tag, data['min_occurs'], data['max_occurs']):
            #     print(f"Occurrence validation failed for element {tag}")
            #     return False

            for tag_content in tag_content_list:
                if data['type'] == 'complex':
                    if not self.validate_xml(tag_content, xsd_data):
                        return False
                else:
                    if not self.validate_type(tag_content, data['type']):
                        print(f"Type validation failed for element {tag}")
                        return False

        return True

    def run(self) -> bool:
        xsd_content = self.read_file(self.XSD_FILE_PATH)
        xml_content = self.read_file(self.XML_FILE_PATH)
        xsd_info = self.extract_xsd_info(xsd_content)
        # breakpoint()
        if self.validate_xml(xml_content, xsd_info):
            print("Validation succeeded")
            return True
        else:
            print("Validation failed")
            return False
