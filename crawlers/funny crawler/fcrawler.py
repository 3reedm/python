#Простой Web-паук 

import sys
import re
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.robotparser import RobotFileParser

class MiniCrawler(HTMLParser):

  viewedQueue=[]
  instQueue=[]
  
  def get_next_link(self):
   if self.instQueue==[]:
    return ""
   else:
    return self.instQueue.pop(0)
	 
  def get_html_file(self,site): 
   try:
    http=urlopen(site)
    httpr=http.read(10000)  #ограничение на скачку
    charset=http.info().get_content_charset()
    html=httpr.decode(charset)
   except:
    print("\n    Неудалось установить соединение.\n    Проверьте подключение к интернету!\n    Возможно был неправильно введён адресс (верно - http://имя_сайта)")
    html=""
   return html

  def handle_starttag(self,tag,attrs):
   if tag=='a':
    newstr=str(attrs[0][1])
    if re.search(r'http|htm|mailto',newstr)!=None:
      if(newstr in self.viewedQueue)==False:
        print("  Добавлено",newstr)
        self.instQueue.append(newstr)
        self.viewedQueue.append(newstr)
    else:
     print("  Игнорированно",newstr)

   
def main():
  print("\nВведите адресс сайта (без http://)")
  site=input()
  if site=="":
   sys.exit(2)
  site="http://"+site
  myCrawler=MiniCrawler()
  #rfParser=RobotFileParser()
  #rfParser.set_url(site)
  #rfParser.read()
  #rfParser.can_fetch("*",site)
  f=open("downloads.txt","w+t",1)
  while site!='':
   print("\nВыполняется попытка подключения к ",site)

   #Скан сайта (не более [n] байтов)
   retfile=myCrawler.get_html_file(site)
  
   #Парсирование сайта (вызов метода handle_starttag), для получения следующих ссылок
   myCrawler.feed(retfile)
   
   #Запись в файл
   if retfile!="":
    f.tell()
    f.write("------------------"+site+"------------------------------------------------"+"\n")
    f.writelines(retfile.text)
    f.write("\n\n\n")
	
   #Получение следующей ссылки
   site=myCrawler.get_next_link()
  
  myCrawler.close()
  f.close()
  
  if retfile!="":
   print("\nПроцесс завершён\n  Найден(о) ",len(myCrawler.viewedQueue)," адресс(ов)")  
 
 #Для запуска файла в качестве импортируемого модуля
if __name__ == "__main__":
   main()