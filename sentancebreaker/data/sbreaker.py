#Простой морфологический анализатор 

import os
import re
import argparse
from sqlite3 import dbapi2 as sqlite

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
    def add_to_index(self,table,field,value,createnew=True):
        cur=self.con.execute(
        "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
            "insert into %s (%s) values ('%s')" % (table,field,value))
        else:
            return

    def get_morpheme(self,table,field,value):
        cur=self.con.execute('select %s from %s where %s="%s"' % (field,table,field,value))
        res=cur.fetchone()
        if res==None:
            return ''
        else:
            return res[0]			
     	
	#Создание таблиц в базе данных
    def create_index_tables(self):
        self.con.execute('create table if not exists rootlist(root)')   
        self.con.execute('create table if not exists prefixlist(prefix)')   
        self.con.execute('create table if not exists suffixlist(suffix)')   
        self.con.execute('create table if not exists endlist(end)')     
        self.con.execute('create index if not exists rootx on rootlist(root)')  
        self.con.execute('create index if not exists prefixx on prefixlist(prefix)')    
        self.con.execute('create index if not exists suffixx on suffixlist(suffix)')    
        self.con.execute('create index if not exists endx on endlist(end)')    		
        self.con.commit()  

class Parser:
    def __init__(self,dbname):
        self.roots=[]
        self.prefixes=[]
        self.suffixes=[]
        self.indexator=Indexator(dbname)
	
    def search_root(self,part):
        root=''
        n=len(part)
        for i in range(n+1):
            for j in range(n-i+1):
                root=part[i:(n-j)]
                root=self.indexator.get_morpheme('rootlist', 'root', root)
                if root and (root in self.roots)==False:
                    self.roots.append(root+' '+str(i)+' '+str(n-j)) 
        self.roots.sort(key=lambda root: -len(root[0:root.find(' ')]))
		    
    def search_prefix(self,part):
        prefix=''
        while not prefix:
            n=len(part)
            for i in range(n+1):
                pre=self.indexator.get_morpheme('prefixlist', 'prefix', part[0:i])
                if pre and (pre in self.prefixes)==False:
                    self.prefixes.append(i) 				
            if not self.prefixes:
                return ''
            self.prefixes.sort(key=lambda pref: -pref)
            for pref in self.prefixes:
                if not part[pref:n]:
                    prefix=part
                    self.prefixes.clear()
                    return prefix
                else:
                    pre=self.indexator.get_morpheme('prefixlist', 'prefix', part[pref:n])
                    if pre:
                        prefix=part[0:pref]+'-'+part[pref:n]
                        self.prefixes.clear()
                        return prefix
            return ''
                
    def search_suffix(self,part):
        suffix=''
        while not suffix:
            n=len(part)
            for i in range(n+1):
                suf=self.indexator.get_morpheme('suffixlist', 'suffix', part[0:i])
                if suf and (suf in self.suffixes)==False:
                    self.suffixes.append(str(i)) 				
            if not self.suffixes:
                return ''
            self.suffixes.sort(key=lambda suff: -int(suff))
            e=0
            for suff in self.suffixes:
                if not part[int(suff):len(part)]:
                    suffix=part
                    self.suffixes.clear()
                    return suffix
                else:
                    p=0
                    while not p:
                        tmp=''
                        if not part[int(suff[len(suff)-1:len(suff)]):len(part)]:
                            ss=suff.split(' ')
                            suffix=part[0:int(ss[0])]
                            for i in range(1,len(ss)):
                                suffix=suffix+'-'+part[int(ss[i-1]):int(ss[i])]
                            self.suffixes.clear()
                            return suffix
                        n=len(part[int(suff[len(suff)-1:len(suff)]):len(part)])
                        for i in range(n+1):
                            suf=self.indexator.get_morpheme('suffixlist', 'suffix', part[int(suff[len(suff)-1:len(suff)]):int(suff[len(suff)-1:len(suff)])+i])
                            if suf:
                                tmp=str(int(suff[len(suff)-1:len(suff)])+i)
                        if not tmp:
                            break
                        suff=suff+' '+tmp
                    self.suffixes[e]=suff
                    e=e+1
            self.suffixes.sort(key=lambda suff: -int(suff[len(suff)-1:len(suff)]))
            break
    
    def search_end(self,part):	
        end=self.indexator.get_morpheme('endlist', 'end', part)
        return end
	
    def search_sin(self,part):
        pass
	
#Запуск
def main():
    
	#Разбор строки в консоли
    argparser=argparse.ArgumentParser()
    argparser.add_argument('-root', type=str, help='Файл с корнями')
    argparser.add_argument('-prefix', type=str, help='Файл с приставками')
    argparser.add_argument('-suffix', type=str, help='Файл с суффиксами')
    argparser.add_argument('-end', type=str, help='Файл с окончаниями')
    argparser.add_argument('-base', type=str, help='Имя базы данных')
    argparser.add_argument('-sentence', type=str, help='Файл со словами')
    args=argparser.parse_args()		
		
    #Создание парсировщика
    parser=Parser(args.base)	
    fr=open(args.root,'rtU')
    fp=open(args.prefix,'rtU')
    fs=open(args.suffix,'rtU')
    fe=open(args.end,'rtU')
    ft=open(args.sentence, 'rtU')
	
	#Создание базы данных частей слова
    for line in fr:
        parser.indexator.add_to_index('rootlist', 'root', line.lower().strip())
    fr.close()
		
    for line in fp:
        parser.indexator.add_to_index('prefixlist', 'prefix', line.lower().strip())
    fp.close()
	
    for line in fs:
        parser.indexator.add_to_index('suffixlist', 'suffix', line.lower().strip())
    fs.close()
	
    for line in fe:
        parser.indexator.add_to_index('endlist', 'end', line.lower().strip()) 
    fe.close()
    parser.indexator.con.commit()
	
    words=[]
    swords=[]
    r=[]
    s=[]
	
    for line in ft:
        
        swords.clear()
        words.clear()
        r.clear()
        s.clear()
		
	    #Считывание слов
        for li in line.split(' '):
            words.append(li.lower().rstrip()) 
	
	    #Деление каждого слова на морфемы
        for word in words:
            rt=''
            prefix=''
            suffix=''
            end='' 
            parts=[]
            flag=True
            while flag:
                parser.roots.clear()
                parser.search_root(word)
                l=len(parser.roots)
                if not l:
                    break
                else:
                    for root in parser.roots:
                        if word==root[0:root.find(' ')]:
                            rt=word
                            flag=False
                            break
                if not flag:
                    continue
                else:
                    i=0
                    for root in parser.roots:
                        parser.prefixes.clear()
                        parser.suffixes.clear()
                        parts.clear()
                        prefix=''
                        suffix=''
                        end=''
                        parts=root.split(' ')
                        parts[1]=word[0:int(parts[1])]
                        if parts[1]:					
                            prefix=parser.search_prefix(parts[1])
                            if not prefix:
                                continue
                        parts[2]=word[int(parts[2]):len(word)]
                        if not parts[2]:
                            rt=parts[0]
                            break						
                        if parts[2]:
                            k=len(parts[2])
                            suffix=parser.search_suffix(parts[2])
                            if suffix:
                                rt=parts[0]
                                break
                            if not parser.suffixes:
                                end=parser.search_end(parts[2])
                                if end:
                                    rt=parts[0]
                                    break
                                else:
                                    continue
                            for suff in parser.suffixes:
                                if not parts[2][suff:k]:
                                    suffix=parts[2]
                                    rt=parts[0]
                                    break
                                end=parser.search_end(parts[2][suff:k])
                                if end:
                                    rt=parts[0]
                                    suffix=parts[2][0:suff]
                                    end=parts[2][suff:k]
                                    break  
                                else:
                                    continue							
							
                    break
            print(word.center(80,':')+'\n'+
		        str('[П]'+prefix+'  '+'[К]'+rt+'  '+'[С]'+suffix+'  '+'[О]'+end+'').center(80)+'\n\n')
            r.append(rt)
            s.append(suffix)
        print(str().center(80,'-')+'\n'+line.center(80,'-'))
        
        for i in range(len(words)):
            if s[i]:
                swords.append(words[i]+' '+str(parser.search_sin(s[i])))
            
        if not len(swords):
            print(str("Предложение не удалось разобрать").center(50)) 
            continue
        else:
            for sword in swords:
                print(sword)
            
    ft.close()
		
		
#Для запуска файла в качестве импортируемого модуля
if __name__:
    main()