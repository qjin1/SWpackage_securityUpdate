import requests
import urllib3
import wget
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

product_list = ['Ericsson product 1414', 'some other product']
vm_list = ['BSS VM SGW1-AMQBRM', 'BSS VM SGW1-ANSIBLE', 'BSS VM SGW1-APACHEPROXY', 'BSS VM SGW1-BRMLDR', 'BSS VM SGW1-BRMORA', 'BSS VM SGW1-BRMPPA', 'BSS VM SGW1-BRMRAT', 'BSS VM SGW1-DBHORA', 'BSS VM SGW1-DOGFS', 'BSS VM SGW1-DWHORA', 'BSS VM SGW1-EXS', 'BSS VM SGW1-GFS', 'BSS VM SGW1-IDMLDAP', 'BSS VM SGW1-JBSAMQ', 'BSS VM SGW1-MONGODB', 'BSS VM SGW1-MONGODBOPS', 'BSS VM SGW1-MZBAT', 'BSS VM SGW1-MZCBS', 'BSS VM SGW1-MZRTI', 'BSS VM SGW1-OCPINF', 'BSS VM SGW1-OCPMAS', 'BSS VM SGW1-OCPNOD', 'BSS VM SGW1-OCPSUP', 'BSS VM SGW1-PPAORA', 'BSS VM SGW1-REPO', 'BSS VM SGW1-RSYSLOG','BSS VM SGW1-SAS', 'BSS VM SGW1-SAPANA', 'BSS VM SGW1-SFTP']

while True:
    product_input = input("Hey user, give your BSS product name: ")
    if product_input not in product_list:
        print("No such product")
    else:
        product_name = product_input
        break


#get the X-AUTH-TOKEN first
token_value = 'xxxxxxxxxxx'

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
    print(vm_name)

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

    # get the csv export for the above product version
    headers = {
        'Accept': 'application/json',
        'X-AUTH-TOKEN': f'{token_value}'
    }

    params = (
        ('format', 'csv'),
    )

    r2 = requests.get(
        f'https://evms-staging.sero.gic.ericsson.se/evms/api/v1/artifacts/versions/{productversion_id}/export',
        headers=headers, params=params, verify=False)
    # print(r2.content)
    #
    #
    ###get the url of the exported csv file
    file_url_jason = r2.json()
    file_url = file_url_jason["path"]
    print('csv file is located in : ' + str(file_url))
    #
    # save to local
    downloaded_csv = wget.download(file_url)
    print('csv file is downloaded to local')

    x = x+1
