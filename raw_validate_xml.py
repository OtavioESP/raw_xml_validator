
class ValidateXML:
    def __init__(self):
        self.FILE_PATH = "./teste.xml"
        self.FINAL_FILE_PATH = "./arquivo_final.txt"
        self.FINAL_DATA = ""

    def sanitize_tag(self, tag: str, remove_dash: bool) -> str:
        return tag.strip("\n").strip(" ")

    def check_father_tags(self, tags: list) -> bool:
        if f'{tags[0].replace("<", "</")}'== tags[ len(tags) - 1 ]:
            return True
        raise ValueError("Elements not inside root tag")


    def check_all_tags_close(self, tags: list) -> bool:
        open_tags_list = []
        close_tags_list = []

        for tag in tags:
            if not "</" in tag and ">" in tag:
                open_tags_list.append(tag)
            elif "<" in tag and ">" in tag:
                close_tags_list.append(tag)

        for t in open_tags_list:
            try:
                close_tags_list.remove(f'{t.replace("<", "</")}')
            except:
                raise ValueError(f"Tag {t} dont have a corresponding close")

        return True

    def check_all_tags_open(self, tags: list) -> bool:
        open_tags_list = []
        close_tags_list = []

        for tag in tags:
            if not "/" in tag:
                open_tags_list.append(tag)
            else: close_tags_list.append(tag)

        for t in close_tags_list:
            try:
                open_tags_list.remove(t.replace("/", ""))
            except:
                raise ValueError(f"Tag {t} dont have a corresponding opening")

        return True

    def check_children_tags(self, tags: list) -> bool:
        tags_depth = {}
        depth_counter = 0

        tags.pop(0)
        tags.pop(len(tags) - 1)

        for tag in tags:
            if all(["<" in tag, ">" in tag, not "</" in tag]):
                depth_counter += 1
                tags_depth[tag] = depth_counter
                self.FINAL_DATA += f'{tag}: '

            if all(["</" in tag, ">" in tag]):
                tags_depth[tag] = depth_counter
                depth_counter -= 1
                self.FINAL_DATA += '\n'

            if not all(["<" in tag,  ">"in tag]) and not "</" in tag:
                self.FINAL_DATA += f'{tag}\n '

        for tag in tags_depth:
            if "<"in tag and not "</" in tag:
                if tags_depth[tag] == tags_depth[tag.replace("<", "</")]:
                    continue
                else:
                    return False
        return True

    def write_txt(self):
        with open(self.FINAL_FILE_PATH, 'w') as file:
            file.write(self.FINAL_DATA)

    def read_file(self) -> list:
        tag_list = []
        lines = open(self.FILE_PATH, 'r').readlines()
        for l in lines:
            sanitized_tag = self.sanitize_tag(l, False)
            tag_list.append(sanitized_tag)

        return tag_list


    def run(self):
        tags = self.read_file()

        if all([self.check_father_tags(tags), self.check_all_tags_close(tags), self.check_all_tags_open(tags), self.check_children_tags(tags)]):
            print(15*'=-=')
            print('VALIDATED !!!')
            print(15*'=-=')
            self.write_txt()
        else:
            print('An error ocurred on validation !')

        print(self.FINAL_DATA)

validar = ValidateXML().run()
