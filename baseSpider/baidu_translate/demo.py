from bd_translate import to_translate

translate_type = [
    {
        'info': '中译英',
        'from': 'zh',
        'to': 'en'
    },
    {
        'info': '英译中',
        'from': 'en',
        'to': 'zh'
    }
]
# 中译英
index = 0
word = "中国"

# # 英译中
# index = 1
# word = "Intratesticular abscess"

current_type = translate_type[index]
res = to_translate(current_type['from'], current_type['to'], word)
print(res)
