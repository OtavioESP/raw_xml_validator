import re

class ValidateXSD:
    def __init__(self):
        self.FILE_PATH = "./teste.xsd"


    def read_file(self) -> list:
        lines = open(self.FILE_PATH, 'r').readlines()
        lines.pop(0)
        lines.pop(len(lines) - 1)
        return lines


    def run(self):
        lines = self.read_file()
        profundidade = 0
        lista = {}
        for key, value in enumerate(lines):
            tag_info = {}
            if '</xs:element' not in value:
                # Tag pai
                if 'xs:element' in value and "/>" not in value:
                    nome = re.search(r'name="(.*?)"', value).group(1)
                    tag_info = dict(profundidade=profundidade, tipo='tag_pai')
                    lista[nome] = tag_info
                    profundidade += 1

                # Tag filha
                elif 'xs:element' in value and "/>" in value:
                    try:
                        nome = re.search(r'name="(.*?)"', value).group(1)
                        tipo = re.search(r'type="(.*?)"', value).group(1)
                        tag_info = dict(profundidade=profundidade, tipo=tipo)
                        lista[nome] = tag_info
                    except AttributeError:
                        breakpoint()

                else:
                    continue

            else:
                profundidade -= 1


        return lista
