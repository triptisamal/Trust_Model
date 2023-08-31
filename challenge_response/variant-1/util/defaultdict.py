from collections import Counter,defaultdict


database = defaultdict(dict)


myid = 0
otherid=1
database[myid][otherid]={}
database[myid][otherid]['name']="one"

otherid=2
database[myid][otherid]={}
database[myid][otherid]['name']="two"
myid = 1
otherid=1112
database[myid][otherid]={}
database[myid][otherid]['name']="weird"

print(database)

for key,val in database.items():
    print("key=",key)
    print("value=",val)
    for k,v in database[key].items():
        print("key=",k)
        print("value=",v)
        for k_in,v_in in database[key][k].items():
            print("key=",k_in)
            print("value=",v_in)
