import json

 
# Opening JSON file
with open('locations.json') as json_file:
    data = json.load(json_file)
 
    # Print the type of data variable
print("Type:", type(data))

# Print the data of dictionary
print("\nmacs:", data['macs'])
print(data['macs'])

macs = data['macs']
names = data['names']
print(macs)


for key, value in macs.items():
    print('Key:', key, 'Value:', value)

for key, value in names.items():
    print('Key', key, 'Value', value)