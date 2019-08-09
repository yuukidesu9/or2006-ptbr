offsets = open('decompiled/header.bin', 'w+b')
strings = open('decompiled/strings.txt', 'w+')
json = open('decompiled/table.json', 'w+')

print('Starting up...')
print('After the dumping, there\'ll be two additional files')
print('in the \'decompiled\' folder: one is \'header.bin\',')
print('containing important offset data, and the other is')
print('\'strings.txt\', containing all the strings dumped')
print('from the file.\n')
print('Now there\'s another file, called \'table.json\'.')
print('Dumping offsets to JSON stream...')
json.write('{\n   \"offsets\": [\"')
print('Dumping from binary file...')
with open('Text/Spanish.bin', 'rb') as infile:
    print('File open successful.')
    content = infile.read(8)
    print('Reading header & offset table. It may take a while...')
    scroller = int.from_bytes(content, 'big')
    content = infile.read(4)
    while content != b'\00\00\00\00':
        le = content[::-1]
        scroller = int.from_bytes(le, 'big')
        offsets.write(le)
        print(str(hex(scroller)))
        json.write(str(hex(scroller)))
        content = infile.read(4)
        json.write('\",\n              \"')
    print('Header and offset table read successfully.')
    json.write('EOF\"],\n   ')
    scroller = int.from_bytes(content, 'big')
    offsets.write(b'\00\00\00\00')
    offsets.close()
    print('Header & offset dump successful.')
    print('Reading string section. Please wait...')
    json.write('\"strings\": [\"')
    content = infile.read(2)
    while content:
        word = str(content)
        scroller = int.from_bytes(content, 'big')
        if content == b'\x00\x00':
            strings.write('\x0d')
            json.write('\",\n      \"')
            #print('Quebra de linha')

        if content == b'\x0a\x00':
            strings.write('#')
            json.write('#')
            #print('Separador de campo')

        if content == b'\x8b\x00':
            strings.write('á')
            json.write('\xe1')

        if content == b'\"\x00':
            strings.write('\"')
            json.write('\"')

        if content == b'\'\x00':
            strings.write('\'')
            json.write('\'')

        if content == b'\x8f\x00':
            strings.write('é')
            json.write('\xe9')

        if content == b'\x93\x00':
            strings.write('í')
            json.write('\xed')

        if content == b'\xcc\x00':
            strings.write('ñ')
            json.write('ñ')

        if content == b'\x97\x00':
            strings.write('ó')
            json.write('\xf3')

        if content == b'\\\x00':
            strings.write('\\')
            json.write('\\')

        if content == b'\x9b\x00':
            strings.write('ú')
            json.write('\xfa')

        if content == b'\xa5\x00':
            strings.write('Á')
            json.write('\xc1')

        if content == b'\xa9\x00':
            strings.write('É')
            json.write('\xc9')
            #print('É')

        if content == b'\xad\x00':
            strings.write('Í')
            json.write('\xcd')
            #print('Í')

        if content == b'\xce\x00':
            strings.write('Ñ')
            json.write('Ñ')
            #print('Ñ')

        if content == b'\xb1\x00':
            strings.write('Ó')
            json.write('\xd3')
            #print('Ó')

        if content == b'\xb5\x00':
            strings.write('Ú')
            json.write('\xda')
            #print('Ú')

        if content == b'\xcf\x00':
            strings.write('¿')
            json.write('¿')
            #print('Interrogação invertida')

        if content == b'\xd0\x00':
            strings.write('¡')
            json.write('¡')
            #print('Exclamação invertida')

        if content == b'\xc9\x00':
            strings.write('™')
            json.write('<')
            #print('Marca Registrada (tm)')

        if content == b'\xca\x00':
            strings.write('©')
            json.write('\xa9')
            #print('Copyright')

        if content == b'\xc8\x00':
            strings.write('®')
            json.write('\xae')
            #print('Marca registrada')

        if content == b'\xcd\x00':
            strings.write('º')
            json.write('\xba')
            #print('Ordinal')

        if content == b'\xa0\x00':
            strings.write('ç')
            json.write('\xe7')
            #print('ç')

        if content == b'\xba\x00':
            strings.write('Ç')
            json.write('\xc7')
            #print('Ç')
        #else:
        strings.write(str(content, 'ascii', 'ignore').strip('\x00'))
        json.write(str(content, 'ascii', 'ignore').strip('\x00'))
        #print(str(content))
        content = infile.read(2)
print('Read successful.')
json.write('EOF\"]\n}')
print('String dump successful.')
print('Dump successful. Exiting now.')
infile.close()
strings.close()