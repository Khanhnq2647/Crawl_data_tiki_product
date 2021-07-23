from bs4 import BeautifulSoup
import re
import csv
import requests
url_list_product_target = []
print("Input number's product target: ",end ="")
number_product = int(input())
for i in range(number_product):
	print("Input product ",i+1,":", end="")
	product_input = input()
	if product_input.split() == 1:
		url = "https://tiki.vn/search?q=" + product_input
		url_list_product_target.append(url)
	else:
		url = "https://tiki.vn/search?q=" + product_input.replace(" ","%20")
		url_list_product_target.append(url)
print(url_list_product_target)

headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:86.0) Gecko/20100101 Firefox/86.0',
          'TE': 'Trailers'
        }
raw_data = []
for url in url_list_product_target:
	response = requests.request("POST", url, headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")
	raw_data.append(soup)
all_item = []
for data in range(len(raw_data)):
	all_products = raw_data[data].find("div", class_ = "ProductList__Wrapper-sc-1dl80l2-0 Kxajl")
	products = all_products.findAll("a", class_ = "product-item")
	print("----------------------------------------------------------------------")
	items = []
	for product in range(len(products)):
		#get price
		price= products[product].find("div", class_ = "price-discount__price").text.replace(" ₫","").replace(".","")
		price = int(price)
	    #get name
		name = products[product].find("div", class_ = "name").text
	    #get quantity_sold
		try:
			quantity_sold = product[product].find("div", class_ = "styles__StyledQtySold-sc-732h27-2 fCfYNm").text
			quantity_sold = re.findall('\\d+', quantity_sold )
	       
		except:
			quantity_sold = "None"
		#get % discount
		try:
			discount = product[product].find("div", class_ = "price-discount__discount").text.replace("%","").replace("-","")
			discount = int(discount)
		except:
			discount = "None"
		item =(name,price,discount,quantity_sold)
		items.append(item)
		print(item)
	all_item.append(items)
	print("Product", data +1)
#save data to txt
file = open("data.txt", mode = "w", encoding = "utf8")
for i in all_item:
	file.write(str(i)+"\n")
