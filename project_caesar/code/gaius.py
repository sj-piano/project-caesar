def script_to_hex(s):
    if s is None:
        return ''
    items = s.split()
    result = ''
    for item in items:
        if item in opcodes:
            result += opcodes[item]
        else:
            result += item
    return result


opcodes = {

    'OP_0': '00',
    'OP_FALSE': '00',

    'OP_DUPLICATE': '76',

    'OP_EQUAL_VERIFY': '88',

    'OP_CHECK_SIGNATURE': 'ac',

    'OP_HASH_160': 'a9',

}

