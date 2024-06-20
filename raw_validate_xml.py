import re

class RawValidateXML:
    '''
    This class aims to validate the .XML file.
    If you want the .XML to be just validated within himself,
    call run() without any paramethers.
    If you want a return file with the validated data,
    call run(true) or run(write_response=True).
    '''
    def __init__(self, file_path: str):
        self.FILE_PATH = file_path
        self.FINAL_FILE_PATH = "./final_file.txt"
        self.FINAL_DATA = ""

    def _sanitize_tag(self, tag: str, remove_dash: bool) -> str:
        return tag.strip("\n").strip(" ")

    def _check_father_tags(self, tags: list) -> bool:
        pattern = r'<([^>\s]+)'
        match_pai = re.search(pattern, tags[0]).group(1)
        match_filho = re.search(pattern, tags[ len(tags) - 1 ]).group(1)
        if match_pai == match_filho[1:]:
            return True

        raise ValueError("Elements not inside root tag")

    def tag_type(self, line: str) -> int:

        # line == ''
        if not line:
            return -2

        if re.fullmatch(r'<(\w+)>', line):
            return 0

        elif re.fullmatch(r'<(\w+)(\s+[^>]*)?>.+<\/\1>', line):
            return 1

        elif re.fullmatch(r'<\/(\w+)>', line):
            return 2

        print(f'Tag {line} não está correta.')
        return -1


    def _check_all_tags_open_close(self, tags: list) -> bool:
        tags.pop(0)
        tags.pop(len(tags) - 1)

        open_tags_list = {}
        close_tags_list = {}

        pattern_open_tag = r'<(\w+)(?:\s+[^>]+)*>'
        pattern_close_tag = r'<\/(\w+)>'

        profundidade = 0

        for tag in tags:
            tag_type = self.tag_type(tag)
            if tag_type == 0:
                tag_name = re.match(pattern_open_tag, tag).group(1)
                profundidade += 1
                open_tags_list[tag_name] = profundidade

            elif tag_type == 2:
                tag_name = re.match(pattern_close_tag, tag).group(1)
                close_tags_list[tag_name] = profundidade
                profundidade -= 1

            elif tag_type == -1:
                return False


        set1 = set(open_tags_list.items())
        set2 = set(close_tags_list.items())

        # se o XML nao foi valido, os sets serao diferentes
        # {tag1: 1 tag2: 2} - {tag1: 1 tag2: 2} == set()
        # {tag1: 1 tag2: 3} - {tag1: 1 tag2: 2} == set(tag2: 3)
        # Retorna as tags ou valores diferentes de um set ou outro
        if len(set1 - set2) != 0:
            print(f'O problema esta na tag: {set1 - set2}, que não fecha.')
            return False

        if len(set2 - set1) != 0:
            print(f'O problema esta na tag: {set2 - set1}, que não abre.')
            return False

        print(len(set1 - set2) == 0 and len(set2 - set1) == 0)

        return True

    def write_txt(self):
        with open(self.FINAL_FILE_PATH, 'w') as file:
            file.write(self.FINAL_DATA)

    def read_file(self) -> list:
        tag_list = []
        lines = open(self.FILE_PATH, 'r').readlines()
        for l in lines:
            sanitized_tag = self._sanitize_tag(l, False)
            tag_list.append(sanitized_tag)

        return tag_list

    def _print_tag_content(self, tags):
        pattern = r'<(\w+)>(.*?)</\1>'
        for item in tags:
            matches = re.findall(pattern, item)
            for tag, data in matches:
                print(f"{tag}: {data.strip()}")

    def run(self, write_response=False):
        tags = self.read_file()
        tags.pop(0)

        if all([self._check_father_tags(tags),self._check_all_tags_open_close(tags)]):
            self._print_tag_content(tags)
            print("VALIDADO")
            return

        print("ERRO")
        return
