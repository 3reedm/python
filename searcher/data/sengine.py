#Простой Web-паук 

import re,os
import argparse
from html.parser import HTMLParser
from sqlite3 import dbapi2 as sqlite
from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

#Паук
class Crawler(HTMLParser):
      
    #Инициализирование паука
    def __init__(self,dbname):
        HTMLParser.__init__(self)
        self.index=Indexator(dbname)
        self.text=''
        self.links=[]
        self.rp=RobotFileParser()
		 
    #Деструктор
    def __del__(self):
        self.close()
  
    #Получение страницы
    def get_html_file(self,url):
        self.text=''
        try:
            web=urlopen(url)
        except URLError as e:
            print(e.reason)
            return
        except TypeError:
            return
        if self.index.is_indexed(url): 
            return
        print("Индексируется",url)
   
        #Проверить на "robots.txt"
        rp_url=urlparse(url)
        self.rp.set_url(rp_url.scheme+'://'+rp_url.netloc+'/robots.txt')
        self.rp.read()
   
        #Получить страницу
        webcode=web.read()
        charset=web.info().get_content_charset()
        try:
            html=webcode.decode(charset)
        except TypeError:
            return
        self.feed(html)
		 
    #Извлечение текста HTML-страницы (без тегов)
    def handle_data(self,data):
        self.text+=" "+data
  
    #Выборка ссылок
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            newstr=str(attrs[0][1])
            if re.search(r'http|htm|html|mailto (?!gif|jpg|png|bmp|tiff|xml)',newstr)!=None:
                if not self.rp.can_fetch("*",newstr):
                    print("Запрещено \"robots.txt\": "+newstr)
                    return
                if not self.index.is_indexed(newstr) and self.rp.can_fetch("*",newstr) and (newstr in self.links)==False:
                    self.links.append(newstr)
   
  
    #Поиск в ширину до заданной глубины
    def crawl(self,pages,depth=1):
        for i in range(depth):
            self.links.clear()
            for page in pages:
                self.get_html_file(page)
                self.index.add_to_index(page,self.text)
 
                for link in self.links:
                    self.get_html_file(link)
                    self.index.add_to_index(link,self.text)
 
                self.index.con.commit()
	
            pages=self.links

#Индексатор
class Indexator:

    #Инициализация индексатора (передача ему имени базы данных)
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)
        self.create_index_tables()		
	
    #Деструктор	
    def __del__(self):
        self.con.close()	
	
	#Функция для получения идентификатора и добавления записи, если такой ещё нет
    def get_entry_id(self,table,field,value,createnew=True):
        cur=self.con.execute(
        "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
            "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
           return res[0]
		   
    #Индексирование одной страницы 
    def add_to_index(self,url,text):
        #Получить список слов
        words=self.separate_words(text)

		#Получить идентификатор URL
        urlid=self.get_entry_id('urllist','url',url)
   
        #Связать каждое слово с этим URL
        for i in range(len(words)):
            word=words[i]
            wordid=self.get_entry_id('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) \
            values(%d,%d,%d)" % (urlid,wordid,i))	 
     
    #Разбиение текста на слова
    def separate_words(self,text):
        splitter=re.compile('\W*')
        return [s.lower() for s in splitter.split(text) if s!='']
  
    #Возвращает true, если данный URL уже проиндексирован
    def is_indexed(self,url):
        u=self.con.execute(
        "select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            #Проверяем, что страница посещалась
            v=self.con.execute(
            "select * from wordlocation where urlid=%d" % u[0]).fetchone()
            if v!=None: 
                return True
        return False
	
	#Создание таблиц в базе данных
    def create_index_tables(self):
        self.con.execute('create table if not exists urllist(url)')
        self.con.execute('create table if not exists wordlist(word)')   
        self.con.execute('create table if not exists wordlocation(urlid,wordid,location)')   
        self.con.execute('create index if not exists wordidx on wordlist(word)')   
        self.con.execute('create index if not exists urlidx on urllist(url)')      
        self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')          
        self.con.commit()   
		 
#Поисковик
class Searcher:
    def __init__(self,dbname):
	    self.con=sqlite.connect(dbname)
		
    def __del__(self):
        self.con.close()
	
    def get_match_rows(self,q):
	    #Строки для построения запроса
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]
        sentences=[]
        nwords=[]
        lwords=''
		
        #Разбить запрос на слова по пробелам
        words=q.split(' ')
        tablenumber=0
		
        for word in words:
		    #Получить идентификатор слова
            wordrow=self.con.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1
            if wordrow==None:
                nwords.append(word)
        if not wordids:
            return []
        if nwords:
            n=len(nwords)
            if n==1:
                print("\n", str("Слово "+nwords[0]+" не найдено в тексте").center(78,'*'))
            else:
                for nword in nwords:
                    lwords+=nword+','+' '
                print("\n", str("Слова "+lwords.rstrip()[:-1]+" не найдены в тексте").center(78,'*'))
		#Создание запроса из отдельных частей
        fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]
		
		#Выделение строки
        i=0
        for row in rows:
            n=len(row)
            sentence=''
			
			#Получение максимального word_id в документе (минимальный 0) 
            fullquery='select location from wordlocation where urlid=%d' % row[0]
            cur=self.con.execute(fullquery).fetchall()
            curs=[row[0] for row in cur]
            max_id=max(curs)
			
			#Если не встретилось таких слов в документе
            if n<2:
                continue			
			#Если встретилось одно слово
            if n==2:
                if row[1]-2>=0:
                    minv=row[1]-2
                else:
                    minv=0
                if row[1]+3<=max_id:
                    maxv=row[1]+3
                else:
                    maxv=max_id
                for locids in range(minv,maxv):
                    fullquery='select wordid from wordlocation where location=%d and urlid=%d' % (locids, row[0])
                    id=self.con.execute(fullquery).fetchone()
                    fullquery='select word from wordlist,wordlocation where location=%d and wordlist.rowid=%d' % (locids, id[0])
                    cur=self.con.execute(fullquery).fetchone()
                    sentence+=cur[0]+' '
			#Больше одного слова (и расстояние между max_id и min_id <=20)
            if n>2:
                rowstmp=[row for row in row]
                rowstmp=rowstmp[1:len(rowstmp)]
                maxv=max(rowstmp)
                minv=min(rowstmp)
                if maxv-minv<=20:
                    if minv-2>=0:
                        minv=minv-2
                    else:
                        minv=0
                    if maxv+3<=max_id:
                        maxv=maxv+3
                    else:
                        maxv=max_id
                    for locids in range(minv,maxv):
                        fullquery='select wordid from wordlocation where location=%d and urlid=%d' % (locids, row[0])
                        id=self.con.execute(fullquery).fetchone()
                        fullquery='select word from wordlist,wordlocation where location=%d and wordlist.rowid=%d' % (locids, id[0])
                        cur=self.con.execute(fullquery).fetchone()
                        sentence+=cur[0]+' '	
            if sentence:
                sentences.append(sentence.rstrip())
		
        return rows,wordids,sentences
		    
		 
#Запуск
def __main__():
    os.environ['HTTP_PROXY']='80.250.174.240:3128'
    os.environ['LANG']='ru_RU.UTF-8' and 'en_US.UTF-8' and 'window-1251'
	
	#Разбор строки в консоли
    parser=argparse.ArgumentParser()
    parser.add_argument('-depth', type=int, help='Глубина проникновения паука внутрь сайта')
    parser.add_argument('-seeds', type=str, help='Файл с начальными узлами')
    parser.add_argument('-base', type=str, help='Имя базы данных')
    args=parser.parse_args()
    
    #Поиск и индексирование сайтов
    crawler=Crawler(args.base)	
    pages=[]	
    for line in open(args.seeds,'rtU'):
        pages.append(line.rstrip())
    crawler.crawl(pages,args.depth)
    
	#Запросы
    searcher=Searcher(args.base)
    q='q'
    ans=[]
    while q:
        print("\n", str("[-----------Введите строку запроса----------]").center(80), "\n")
        q=str(input(str('').center(18,'>'))).lower().replace('\'','\"')
        if q=='': 
            break 
        ans=searcher.get_match_rows(q)
        if not ans:
            print("\n", str("Слова в строке запроса не найдены в тексте").center(78, '*'))
            continue
        print("\n\n", str("DOC_id, DOC_word[k]_id - прямой индекс:").center(80), "\n")
        for an in ans[0]:
            print(" ", an)
        print("\n", str("WORD[k]_id - обратный индекс:").center(80), "\n")
        for an in ans[1]:
            print(" ", an)		
        if ans[2]:
            print("\n", str("Строки(по порядку DOC_id):").center(80), "\n", str("(если длина строки не больше 20 слов):").center(80), "\n\n")
            i=1
            for an in ans[2]:
                print(" [", i, "]  ", an, end="\n\n")
                i+=1				
		
#Для запуска файла в качестве импортируемого модуля
if __name__=='__main__':
    __main__()