from bs4 import BeautifulSoup
import urllib.request as req
import urllib
from time import sleep
import re
import csv
import datetime
##################################
#       SETTINGS
##################################

date = datetime.datetime.now()
tstamp = '%04d%02d%02d' % (date.year, date.month ,date.day)

OUT_F = 'output/HydroStations_%s.csv' % tstamp
LOG_F  = r".\log\log%s.log" % tstamp
BASE_URL = "http://fccj.jp/hystation/"
err_url = "https://baseball.yahoo.co.jp/mlbdfadf/"

###################################
#       METHODS
###################################

	
def write_log(file,str):
	f_logout = open(file,'a')
	f_logout.writelines(str + "\n")
	f_logout.close()
	
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


def get_soup(url):
	
	try:
		res = req.urlopen(url)
		soup = BeautifulSoup(res,'html.parser')
		return soup
		
	except urllib.error.HTTPError as http_e:
		print( http_e.code , http_e.reason, url)
		log_str = str( http_e.code) + http_e.reason +  url
		write_log(LOG_F, str(http_e.code)  )
	except Exception as e:
		print(e)


##################################
#       EXECUTION
##################################


if __name__ == '__main__':

	soup = get_soup(err_url)
	soup = get_soup(BASE_URL)
	
	for tr in soup.findAll('tr'):
		
		for a_tag in tr.findAll('a'):
			if a_tag.get("class"):
				pass

			else:
				
				st_url = BASE_URL + a_tag.get("href")
				st_name = a_tag.get_text()
				
				
				st_soup = get_soup(st_url)
				
				st_address= get_address(st_soup)
				
				st_lat,st_lon = get_geopoint(st_soup)
				
				info_list = [st_name,st_address,st_lat,st_lon,st_url]
				print(info_list)
				write_info(OUT_F,info_list)
				
				sleep(1.5)
			
	

