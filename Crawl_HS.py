from bs4 import BeautifulSoup
import urllib.request as req
from time import sleep
import re
import csv

###################################
#       METHODS
###################################

def write_info(f_name,info_list):
	
	f_out = open(f_name,'a')
	writer = csv.writer(f_out,lineterminator='\n')
	
	try:
		writer.writerow(info_list)

	except UnicodeEncodeError as e:
		pass
	
	finally:
		f_out.close()
	

def get_address(soup):
	
	i = 1
	for td in st_soup.findAll('td'):
		address = td.get_text()
		if i ==2: return address
		i += 1


def get_geopoint(soup):
	
	for div in soup.findAll('script'):
		point_script = div.text.replace("\xa9","a")
		if point_script .find('var lat = ') > 1:
			st_point_list = re.findall('\d+(?:\.\d+)?',point_script)
			st_lat = st_point_list[0]
			st_lon = st_point_list[1]
			return st_lat,st_lon



##################################
#       SETTINGS
##################################

f_out = 'output/chain_info.csv'
url = "http://fccj.jp/hystation/"



##################################
#       EXECUTION
##################################


if __name__ == '__main__':
	
	res = req.urlopen(url)
	soup = BeautifulSoup(res, 'html.parser')
	
	for tr in soup.findAll('tr'):
		
		for a_tag in tr.findAll('a'):
			if a_tag.get("class"):
				pass

			else:
				
				st_url = url + a_tag.get("href")
				st_name = a_tag.get_text()
				
				st_res = req.urlopen(st_url)
				st_soup = BeautifulSoup(st_res,'html.parser')
				
				st_address= get_address(st_soup)
				
				st_lat,st_lon = get_geopoint(st_soup)
				
				info_list = [st_name,st_address,st_lat,st_lon,st_url]
				print(info_list)
				write_info(f_out,info_list)
				
				sleep(1.5)
			


