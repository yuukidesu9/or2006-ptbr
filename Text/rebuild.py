import binascii

strings = open('decompiled/strings.txt', 'r')
header = open('decompiled/header.bin', 'rb')

with open('output/patch.bin', 'wb+') as patched:
    patched.write(b'txet')
    patched.write(b'\x78\x56\x34\x12')
    head = header.read(4)
    while head:
        data = head[::-1]
        scroll = int.from_bytes(head, 'big')
        patched.write(data)
        head = header.read(4)
    header.close()
    string = strings.read(1)
    while string:
        stra = bytes(string, 'cp1252', 'ignore')
        scroll = int.from_bytes(stra, 'big')
        if stra == b'\x0d':
            patched.write(b'\x00') # Quebra de campo (\r)

        if stra == b'\x23':
            patched.write(b'\x0a') # Quebra de linha (#)

        if stra == b'\xe7':
            patched.write(b'\xa0') # ç

        if stra == b'\xc7':
            patched.write(b'\xba') # Ç

        if stra == b'\xe1':
            patched.write(b'\x8b') # á

        if stra == b'\xe0':
            patched.write(b'\x8a') # à

        if stra == b'\xe2':
            patched.write(b'\x8c') # â

        if stra == b'\xe3':
            patched.write(b'\xcc') # ã (ñ)

        if stra == b'\xe9':
            patched.write(b'\x8f') # é

        if stra == b'\xea':
            patched.write(b'\x90') # ê

        if stra == b'\xed':
        #if stra == 'í':
            patched.write(b'\x93') # í

        if stra == b'\xf3':
            patched.write(b'\x97') # ó
        
        if stra == b'\xf4':
            patched.write(b'\x98') # ô

        if stra == b'\xf5':
            patched.write(b'\xd0') # õ (exclamação invertida)

        if stra == b'\xfa':
            patched.write(b'\x9b') # ú

        if stra == b'\xc1':
            patched.write(b'\xa5') # Á

        if stra == b'\xc0':
            patched.write(b'\xa4') # À

        if stra == b'\xc2':
            patched.write(b'\xa6') # Â

        if stra == b'\xc3':
            patched.write(b'\xce') # Ã (Ñ)

        if stra == b'\xc9':
            patched.write(b'\xa9') # É

        if stra == b'\xca':
            patched.write(b'\xaa') # Ê

        if stra == b'\xcd':
            patched.write(b'\xad') # Í

        if stra == b'\xd3':
            patched.write(b'\xb1') # Ó

        if stra == b'\xd4':
            patched.write(b'\xb2') # Ô

        if stra == b'\xd5':
            patched.write(b'\xcf') # Õ (interrogação invertida)

        if stra == b'\xda':
            patched.write(b'\xb5') # Ú

        if stra == b'\x99':
            patched.write(b'\xc9') # tm

        if stra == b'\xa9':
            patched.write(b'\xca') # (c)

        if stra == b'\xae':
            patched.write(b'\xc8') # (R)

        if stra == b'\xba':
            patched.write(b'\xcd') # ordinal

        if stra == b'\x0d':
            print('', end='') # \n

        if stra == b'\x0d':
            print('', end='') # \r
        else:
            patched.write(bytes(string, 'ascii', 'ignore'))
        
        print(string, end='')
        patched.write(b'\x00')
        string = strings.read(1)
strings.close()
patched.close()
# -------------------------------------------------------------------
# - Abrir script
# - Espaçar caracteres, lembrando que:
#     > um '&' equivale a 00
#     > um '$' equivale a 0A
# ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# A tabela mais completa será codada aqui. ^w^
# -------------------------------------------------------------------
# Juntar cabeçalho ,lembrando que é a string ASCII 'text' (no
# arquivo original, é 'txet', por estar em little endian) e
# depois o tamanho do arquivo em hex [0x11223344] (que também
# está em little endian, sendo 0x44332211).
# Daí vem os offsets, que estão no mesmo formato, ou seja:
#####################################################################
#      conteúdo       |            descrição           |   offset
# --------------------|--------------------------------|------------
#  t    x    e    t   | (magic do cabeçalho)           | 0x00000000
# 0x44 0x33 0x22 0x11 | (tamanho do arquivo, em bytes) | 0x00000004
# <44  33   22   11>  | (offset #1)                    | 0x00000008
# <44  33   22   11>  | (offset #2)                    | 0x0000000c
#     .    .    .     |                                |    . . .
# 0x00 0x00 0x00 0x00 | (separador)                    | 0x00001538
#  S   0x00  t   0x00 |                                | 0x0000153c
#  r   0x00  i   0x00 |                                | 0x00001540
#  n   0x00  g   0x00 | (strings, com cada caractere   | 0x00001544
# 0x00 0x00  S   0x00 | separado por 0x00, depois por  | 0x00001548
#  t   0x00  r   0x00 | mais dois 0x00's)              | 0x0000154c
#  i   0x00  n   0x00 |                                | 0x00001550
#  g   0x00 0x00 0x00 |                                | 0x00001554
#     .    .    .     |                                |    . . .
# -------------------------------------------------------------------
# - Fechar arquivo final
# -------------------------------------------------------------------