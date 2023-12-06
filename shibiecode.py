import easyocr
reader = easyocr.Reader(['ch_sim', 'en'])

result = reader.readtext(f'code.png')
print(result)
for item in result:
    print(item[1])