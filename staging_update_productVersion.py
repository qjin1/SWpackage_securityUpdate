import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

product_list = ['Ericsson product 1414', 'some other product']
vm_list = ['BSS VM SGW1-ANSIBLE', 'BSS VM SGW1-SAS']

while True:
    product_input = input("Hey user, give your BSS product name: ")
    if product_input not in product_list:
        print("No such product")
    else:
        product_name = product_input
        break



while True:
    vm_input = input("give your vm name: ")
    if vm_input.upper() not in vm_list:
        print("No such virtual machine")
    else:
        vm_name = vm_input.upper()
        break

upload_filename = input("give your new upload csv file name: ")
print('you are uploading:' , f'{upload_filename}')

#get the X-AUTH-TOKEN first
token_value = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlcW5paWpuIiwiZXhwIjoxNjQ2MzU0NTQ5fQ.52cvx0mXCOFmixtzNZZw1xG7YWJBOqBO_Ay_ozKDdJc'

# get the product name and id list
headers = {
    'Accept': 'application/json',
    'X-AUTH-TOKEN': f'{token_value}',
}
r = requests.get('https://evms-staging.sero.gic.ericsson.se/evms/api/1/artifacts/products', headers=headers, verify=False)
#print(r.content)
product_dict = r.json()

#get product id
for i in product_dict:
    #print(product_dict[0]['name'])
    if i["name"] == f'{product_name}':
        id_BS1 = i['id']
        print(f'product_id of {product_name} is: ' + str(id_BS1))
    else:
        None

#
#get product version_id
headers = {
    'Accept': 'application/json',
    'X-AUTH-TOKEN': f'{token_value}',
}

r1 = requests.get(f'https://evms-staging.sero.gic.ericsson.se/evms/api/v1/artifacts/products/{id_BS1}/versions', headers=headers, verify=False)
#print(r1.content)
version_dict = r1.json()
for i in version_dict:
    #print (i['id'], i['version'])
    if i["version"] == f'{vm_name}':
        productversion_id = i['id']
        print (f'product version id of {vm_name} is: ' + str(productversion_id))
    else:
        None
#
#
#upload the product version with csv file
headers = {
    'Accept': 'application/json',
    'X-AUTH-TOKEN': f'{token_value}',
}

files = {
'file': (f'{upload_filename }', open(f'{upload_filename }', 'rb')),
}

r2 = requests.post(f'https://evms-staging.sero.gic.ericsson.se/evms/api/v1/artifacts/versions/{productversion_id}/upload', headers=headers, files=files, verify=False)
print(r2.content)