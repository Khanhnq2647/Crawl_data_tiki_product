from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
file = open("items_target.txt", mode = "r", encoding ="utf8")
add_dress = file.read()
page_number = 1
urls = []
for i in range(1,page_number+1):
	url = add_dress + "&page=" + str(i)
	urls.append(url)

def get(urls):
	items = []
	for url in urls:
	    html = urlopen(url).read()
	    soup_packtpage = BeautifulSoup(html, "html.parser")
	    res = soup_packtpage.find('div', attrs = {"class":"ProductList__Wrapper-sc-1dl80l2-0 Kxajl"})
	    product = res.findAll("a", class_ = "product-item")
	for pro in product:
	    gia= pro.find("div", class_ = "price-discount__price").text.replace(" ₫","").replace(".","")
	    price = int(gia)
	    name = pro.find("div", class_ = "name").text
	    try:
	        soluongdaban = pro.find("div", class_ = "styles__StyledQtySold-sc-732h27-2 fCfYNm").text
	        quantity_sold = re.findall('\\d+', soluongdaban )
	       
	    except:
	        quantity_sold = "None"
	    try:
	        giamgia = pro.find("div", class_ = "price-discount__discount").text.replace("%","").replace("-","")
	        discount = int(giamgia)
	    except:
	        discount = "None"
	    item =[name,price,discount,quantity_sold]
	    listToStr =  ','.join(map(str, item))
	    items.append(listToStr)
	return items
data = get(urls)
print(data)
#save data to txt
file = open("data.txt", mode = "w", encoding = "utf8")
for i in data:
    file.write(i+str("\n"))