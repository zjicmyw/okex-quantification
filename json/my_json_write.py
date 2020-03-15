import json

accounts = {


}

# 如果你要处理的是文件而不是字符串，你可以使用json.dump()和json.load()来编码和解码JSON数据。

# 把字典类型写入到文件中
# with open("json/accounts.json", "w") as f:
#     json.dump(accounts, f)

# load:把文件打开，并把字符串变换为数据类型
with open("json/accounts.json", 'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict)