import  json

str = [{"username":"杨科威廉","age":24},(2,3),1]
json_str = json.dumps(str,ensure_ascii=False)
print(json_str)

new_str = json.loads(json_str)
print(new_str)
