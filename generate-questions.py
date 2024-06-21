from urllib import request
import os
from selenium import webdriver
from bs4 import BeautifulSoup

def get_href(tag):
  return tag.attrs['href']

def verify_class_tag(tag):
  return "class" not in list(tag.attrs)

def download_pdf(lnk):
  options = webdriver.ChromeOptions()
    
  download_folder = os.getcwd()  
  
  profile = {"plugins.plugins_list": [{"enabled": False,
                                        "name": "Chrome PDF Viewer"}],
              "download.default_directory": download_folder,
              "download.extensions_to_open": "",
              "plugins.always_open_pdf_externally": True}
  
  options.add_experimental_option("prefs", profile)
      
  driver = webdriver.Chrome(options = options)
  driver.get(lnk)
  
  driver.close()

response = request.urlopen("https://www.sbc.org.br/documentos-da-sbc/category/153-provas-e-gabaritos-do-poscomp")
html = response.read().decode('UTF-8')
soup = BeautifulSoup(html, "html.parser")

for tag in soup.find_all():
  if(verify_class_tag(tag)):
    continue
  if("jd_categories_title39" in tag.attrs['class']):
    page_year = request.urlopen("https://www.sbc.org.br" + get_href(tag.contents[0])).read().decode('UTF-8')
    soup_year = BeautifulSoup(page_year, 'html.parser')
    links = []
    for year_tag in soup_year.find_all():
      if(verify_class_tag(year_tag)):
        continue
      if("jd_download_url" in year_tag.attrs['class']):
        links.append(get_href(year_tag))
      
    links = links[::-1]
    for link in links:
      page_donwload = request.urlopen("https://www.sbc.org.br" + link).read().decode('UTF-8')
      soup_download = BeautifulSoup(page_donwload, 'html.parser')
      for tag_download in soup_download.find_all():
        if("title" not in list(tag_download.attrs)):
          continue
        if("Start downloading" in tag_download.attrs['title']):
          download_pdf("https://www.sbc.org.br" + get_href(tag_download))
          print(os.listdir())
    