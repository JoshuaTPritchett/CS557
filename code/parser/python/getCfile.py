import json
jsonfile = 'C:\Users\pools\Downloads\\answers-15-sec-run\\answers-15-sec-run.json'
with open(jsonfile) as data_file:
    data = json.load(data_file)

index = 0
for index in range(len(data)):
    filename = str(data[index]["AnswerId"]) + "_" + str(data[index]["ParentId"]) + "_" + str(data[index]["Score"]) + "_" + str(data[index]["OwnerUserId"]) + ".c"
    with open(filename, 'a') as the_file:
        the_file.write(data[index]["Code"].encode("utf-8"))


