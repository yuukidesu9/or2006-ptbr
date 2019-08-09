import argparse
import textwrap
import sys
import json

class Dumper(object):

    offsets = []
    strings = []

    control_bytes = {
        b'\x00\x00'     :   '\n',
        b'\x0a\x00'     :   '#',
        b'\x8b\x00'     :   'á',
        b'\"\x00'       :   '\"',
        b'\'\x00'       :   '\'',
        b'\x8f\x00'     :   'é',
        b'\x93\x00'     :   'í',
        b'\xcc\x00'     :   'ñ',
        b'\x97\x00'     :   'ó',
        b'\\\x00'       :   '\\',
        b'\x9b\x00'     :   'ú',
        b'\xa5\x00'     :   'Á',
        b'\xa9\x00'     :   'É',
        b'\xad\x00'     :   'Í',
        b'\xce\x00'     :   'Ñ',
        b'\xb1\x00'     :   'Ó',
        b'\xb5\x00'     :   'Ú',
        b'\xcf\x00'     :   '¿',
        b'\xd0\x00'     :   '¡',
        b'\xc9\x00'     :   '™',
        b'\xca\x00'     :   '©',
        b'\xc8\x00'     :   '®',
        b'\xcd\x00'     :   'º',
        b'\xa0\x00'     :   'ç',
        b'\xba\x00'     :   'Ç'
    }

    def __init__(self, data):
        # Cria os arquivos de output
        self.decompiled_headerbin_output = open('./decoded/header.bin', 'wb+')
        self.decompiled_offsets_output = open('./decoded/offsets.json', 'w+')
        self.decompiled_strings_output = open('./decoded/strings.json', 'w+')

        # Transforma o conteudo do arquivo de entrada em Classe do tipo Objeto
        self.binary = BinaryFile(data)

        # Inicia o processo
        self.start()

    def start(self):

        # Pula os primeiros 8 bytes iniciais
        debug = self.binary.skip(8)

        # Le a tabela de offsets no header
        while True:
            data = self.binary.read(4)
            if data.value == b'\x00\x00\x00\x00':
                break
            # Inverte o valor do offset
            reversed_data = BinaryBytes(data.value[::-1])
            # Adiciona o valor do offset a lista
            self.offsets.append(hex(reversed_data.as_integer))
            # Escreve o offset no arquivo binario
            self.decompiled_headerbin_output.write(reversed_data.value)

        # Exporta a lista de offsets como JSON
        json.dump(self.offsets, self.decompiled_offsets_output, indent=4, ensure_ascii=False)
        
        # Le as strings do conteudo
        text = ""
        while True:
            if self.binary.current_offset >= self.binary.end_offset:
                break
            data = self.binary.read(2)
            if data.value in self.control_bytes:
                # Se for quebra de linha adiciona a lista
                if self.control_bytes[data.value] == '\n':
                    self.strings.append(text)
                    text=""
                # Caso não atribui a string
                else:
                    tmp = self.control_bytes[data.value]
                    text += tmp
            else:
                # Corta o 0x00 do bytes utf-8
                text += data.as_string
        
        # Exporta a lista de strings como JSON
        json.dump(self.strings, self.decompiled_strings_output, indent=4, ensure_ascii=False)
            
class BinaryFile(object):

    def __init__(self, data):
        # Define o offset inicial do arquivo e a posição atual pro mesmo
        self.start_offset = 0
        self.current_offset = 0

        # Define o conteudo do arquivo
        self.content = data

        # Define o EOF do arquivo
        self.end_offset = len(data)

    """ Função para leitura dos bytes """
    def read(self, nbytes):
        # Atribui o valor do offset atual de leitura + o numero de bytes desejados
        value = self.content[self.current_offset:(self.current_offset+nbytes)]
        # Incrementa o offset atual de leitura
        self.current_offset += nbytes
        return BinaryBytes(value)

    """ Função para pular n bytes """
    def skip(self, nbytes):
        self.current_offset += nbytes


class BinaryBytes(object):
    def __init__(self, byte_value):
        self.value = byte_value
        # Converte o byte para inteiro
        self.as_integer = int.from_bytes(byte_value, 'big')
        # Tenta decodificar o conteúdo como UTF-8 senão atribui NULL
        try:
            self.as_string = str(byte_value.decode("utf-8")).strip('\u0000')
        except Exception:
            self.as_string = ""

if __name__ == '__main__':
    """ Program Command Line """
    cmd = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            [OR2006] TEXT DECODER
            --------------------------------------------------
            python decoder.py input
            --------------------------------------------------
            After the dumping, there\'ll be two additional files
            in the \'decompiled\' folder: one is \'header.bin\'
            containing important offset data, and the other is
            \'strings.txt\', containing all the strings dumped
            'from the file.
        ''')
    )

    cmd.add_argument(
        'infile',
        nargs='?',
        type=argparse.FileType('rb'),
        default=sys.stdin,
        help='Input file.'
    )

    """ Program Main Routine """
    args = cmd.parse_args()

    if(args.infile.name != '<stdin>'):
        with args.infile as input_file:
            content = input_file.read()
        Dumper(content)
    else:
        cmd.print_help()