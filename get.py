from bs4 import BeautifulSoup
import re
import csv
import requests
url_list_product_target = []
print("Input number's product target: ",end ="")
number_product = int(input())
for i in range(number_product):
	print("Input product",i+1,": ", end="")
	product_input = input()
	if product_input.split() == 1:
		url = "https://tiki.vn/search?q=" + product_input
		url_list_product_target.append(url)
	else:
		url = "https://tiki.vn/search?q=" + product_input.replace(" ","%20")
		url_list_product_target.append(url)
print("Input number's page, you want crawl:", end ='')
number_page = int(input())
#print(url_list_product_target)
print("Number of page is:", number_page)
print("Total Number is: ",number_page*number_product)
headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:86.0) Gecko/20100101 Firefox/86.0',
          'TE': 'Trailers'
        }
# write header to csv
with open("clean_data.csv", encoding="utf8", mode="w", newline='') as file_csv:
	header = ["Name", "Price", "Discount","Quantity Sold"]
	writer = csv.writer(file_csv)
	writer.writerow(header)

raw_data = []
for url in url_list_product_target:
	for i in range(1,number_page+1):
		url_page = url + "&page="+ str(i)
		response = requests.request("POST", url_page, headers=headers)
		soup = BeautifulSoup(response.text, "html.parser")
		raw_data.append(soup)
all_item = []
for data in range(len(raw_data)):
	all_products = raw_data[data].find("div", class_ = "ProductList__Wrapper-sc-1dl80l2-0 Kxajl")
	products = all_products.findAll("a", class_ = "product-item")
	print("Done page:",data+1)
	for product in range(len(products)):
		for info in products[product]:
			#get price
			price= info.find("div", class_ = "price-discount__price").text.replace(" ₫","").replace(".","")
			price = int(price)
		    #get name
			name = info.find("div", class_ = "name").text
		    #get quantity_sold
			try:
				quantity_sold = info.find("div", class_ = "styles__StyledQtySold-sc-732h27-2 fCfYNm").text
				quantity_sold = re.findall('\\d+', quantity_sold )
				quantity_sold = quantity_sold[0]
		       
			except:
				quantity_sold = "None"
			#get % discount
			try:
				discount = info.find("div", class_ = "price-discount__discount").text.replace("%","").replace("-","")
				discount = int(discount)
			except:
				discount = "None"
			item =[name,price,discount,quantity_sold]
			
			
			with open("clean_data.csv", "a", encoding='utf-8', newline='') as file_csv:
				writer = csv.writer(file_csv)
				writer.writerow(item)
	