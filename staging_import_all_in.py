import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

product_list = ['Ericsson product 1414', 'some other product']
vm_list = ['BSS VM SGW1-AMQBRM', 'BSS VM SGW1-ANSIBLE', 'BSS VM SGW1-APACHEPROXY', 'BSS VM SGW1-BRMLDR', 'BSS VM SGW1-BRMORA', 'BSS VM SGW1-BRMPPA', 'BSS VM SGW1-BRMRAT', 'BSS VM SGW1-DBHORA', 'BSS VM SGW1-DOGFS', 'BSS VM SGW1-DWHORA', 'BSS VM SGW1-EXS', 'BSS VM SGW1-GFS', 'BSS VM SGW1-IDMLDAP', 'BSS VM SGW1-JBSAMQ', 'BSS VM SGW1-MONGODB', 'BSS VM SGW1-MONGODBOPS', 'BSS VM SGW1-MZBAT', 'BSS VM SGW1-MZCBS', 'BSS VM SGW1-MZRTI', 'BSS VM SGW1-OCPINF', 'BSS VM SGW1-OCPMAS', 'BSS VM SGW1-OCPNOD', 'BSS VM SGW1-OCPSUP', 'BSS VM SGW1-PPAORA', 'BSS VM SGW1-REPO', 'BSS VM SGW1-RSYSLOG','BSS VM SGW1-SAS', 'BSS VM SGW1-SAPANA', 'BSS VM SGW1-SFTP']

while True:
    product_input = input("Hey user, give your BSS product name: ")
    if product_input not in product_list:
        print("No such product")
    else:
        product_name = product_input
        product_name_no_space = product_input.replace(" ", "")
        break

#upload_filename = input("give your new upload csv file name: ")
#print('you are uploading:' , f'{upload_filename}')

#get the X-AUTH-TOKEN first
token_value = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlcW5paWpuIiwiZXhwIjoxNjUyNzQxNTk5fQ.iVymPNxFEPaWlKJJYdX7X9qwhBE3QzJXHeKwHEzVrXA'

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

x = 0
# Iterating using while loop
while x < len(vm_list):
    vm_name = vm_list[x]
    vm_name_no_space = vm_name.replace(" ", "")
    print(vm_name)
    file_ending = ".csv"
    upload_filename = product_name_no_space + vm_name_no_space + file_ending
    print('uploading csv file : ' + str(upload_filename))


#
#get product version_id
    headers = {
        'Accept': 'application/json',
        'X-AUTH-TOKEN': f'{token_value}',
    }

    r1 = requests.get(f'https://evms-staging.sero.gic.ericsson.se/evms/api/v1/artifacts/products/{id_BS1}/versions',
                      headers=headers, verify=False)
    # print(r1.content)
    version_dict = r1.json()
    for i in version_dict:
        # print (i['id'], i['version'])
        if i["version"] == f'{vm_name}':
            productversion_id = i['id']
            print(f'product version id of {vm_name} is: ' + str(productversion_id))
        else:
            None
    #
    #
    # upload the product version with csv file
    headers = {
        'Accept': 'application/json',
        'X-AUTH-TOKEN': f'{token_value}',
    }

    files = {
        'file': (f'{upload_filename}', open(f'{upload_filename}', 'rb')),
    }

    r2 = requests.post(
        f'https://evms-staging.sero.gic.ericsson.se/evms/api/v1/artifacts/versions/{productversion_id}/upload',
        headers=headers, files=files, verify=False)
    print(r2.content)

    x = x + 1