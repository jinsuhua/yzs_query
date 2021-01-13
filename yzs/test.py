import json

dir = "D:\\tmp\\test\\unzip\\20201217\\2020.12.09.13.45.29.188-d09afc5474014d61a20577ef4c4a17f9\\10.129.97.10^3306^metadata_test^null\\asc_dealer_mapping\\columns.json"
with open(dir, encoding='utf-8') as f:
    data = f.read()
    ff = json.loads(data)
    print(ff)

    for i in ff:
        col = i.get("columnName")
        print(col)