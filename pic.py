import easyocr
import re
if __name__ == '__main__':
    reader = easyocr.Reader(['ch_sim', 'en'])

    result = reader.readtext('t.png')
    pattern = r"(?P<key>[\u4e00-\u9fa5a-zA-Z]+)[:：]\s*(?P<value>\d+(?:\.\d+)?)"
    # 使用正则表达式匹配冒号后的数值
    matches = re.findall(pattern, result[0][1])
    # 构建字典，按照元组的第一个元素作为键，第二个元素作为值
    dic = {key: value for key, value in matches}
    print(dic)