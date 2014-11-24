defs = {'std': '標準', 'string': '繩子', 'namespace': '名字洞', 'main': '主要', 'name': '名字', 'endl': '換行', 'using': '使用', 'cin': '吸入', 'int': '整數', '0': '零', 'return': '傳回', 'cerr': '吸不到', 'cout': '吸出'}

def htmlConvert(s):
    for key, value in defs.items():
        s.replace('>{}<'.format(key), '>{}<'.format(value))
    return s
