#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

/**

Форма Бекуса-Наура. Программа

//Составить синтаксический анализатор для грамматики, похожей на эту:

<Существительное>::=Дом|Человек|Пёс
<Прилагательное>::=Старый|Огромный|Далёкий
<Глагол>::=Стоял|Виднелся|Был

<Сказуемое>::=<Глагол>
<Подлежащее>::=<Прилагательное> <Существительное>
<Дополнение>::=<Прилагательное> <Существительное>

<Предложение>::=<Подлежащее> <Сказуемое> <Дополнение>

**/

 std::vector<std::vector<std::string> > ReadFileGram(std::string);
 std::vector<std::vector<std::string> > ReadFileEx(std::string);
 std::string Create(std::vector<std::vector<std::string> >);
 bool Destruct(std::vector<std::vector<std::string> >, std::vector<std::string>);
 
int main(){
 int i,j;
 std::vector<std::vector<std::string> > gram;
 std::vector<std::vector<std::string> > examples;
 gram=ReadFileGram("gram.txt");                      //Считывание грамматики
 examples=ReadFileEx("examples.txt");                //Считывание примеров предложений
 
 //Для генерирования предложений, используя грамматику
 //Цикл для печати
 std::cout<<std::endl<<"-----------------------------Построение предложений-----------------------------"<<std::endl;                            
 for(i=0; i<5; ++i){                    
  std::cout<<i+1<<". "<<Create(gram)<<std::endl;
 }
 
 //Для проверки на принадлежность грамматике  
 //Цикл для печати
 std::cout<<std::endl<<"---------------------Проверка на принадлежность грамматике----------------------"<<std::endl;
 for(i=0; i<examples.size(); ++i){
  std::cout<<i+1<<". \"";
  for(j=0; j<examples[i].size(); ++j){
   if(j!=examples[i].size()-1)  
    std::cout<<examples[i][j]<<" ";
   else
    std::cout<<examples[i][j];
  }
  std::cout<<"\"";
  if(Destruct(gram, examples[i])==true)       
   std::cout<<" принадлежит грамматике"<<std::endl;
  else
   std::cout<<" не принадлежит грамматике"<<std::endl;
 }
 
 return 0;
}

 
 std::vector<std::vector<std::string> > ReadFileGram(std::string FilePath){ 
  int i,j,k,t,l1,l2;
  std::string str; 
  std::vector<int> count;  
  std::vector<std::string> m_str;                //Вектор для считывания построчно с файла
  std::vector<std::string> l_str;                //Временный вектор для одной строки 
  std::vector<std::vector<std::string> > ml_str; //Вектор результата
  
  //////////////////Получение грамматики с файла//////////////////////
  std::ifstream fin(FilePath.c_str());    
  if(!fin){
   std::cout<<"File error!"<<std::endl;
   std::exit(0);
  }
  while(getline(fin,str)) 
    m_str.push_back(str);
  fin.close();
  
  /////////////////Выделение слов////////////////////
  std::string delims;                 /*" :=|<>"*/                            //Служебные нетерминальные символы "|" - или (or); "::=" - отделение левой части от правой; "<>" - В скобках указаны любые производные терминалы; " " - и (and).
  const std::string choose("|");      /*"[{/|"*/                              //Можно добавить символы, которые тоже увеличивают возможность выбора, повтора.
  std::string::size_type end_pos;
  std::string::size_type choose_pos;
  std::string::size_type beg_pos;
  std::string tmp;                                                     //Для подстроки
  /////////////////Деление на слова
  for(i=0; i<m_str.size(); ++i){
   delims=" :=|<>";
   choose_pos=m_str[i].find_first_of(choose);
   if(choose_pos!=std::string::npos)
    delims=":=|<>";
   beg_pos=m_str[i].find_first_not_of(delims);
   while (beg_pos!=std::string::npos){
     //Определение конца слова
     end_pos=m_str[i].find_first_of(delims,beg_pos);
	 
     //Запись слова
     tmp.insert(0,m_str[i].substr(beg_pos, end_pos == std::string::npos // ?? end_pos ???"not found"
	                                 ? std::string::npos                // ???"all remaining characters"
                                     : end_pos - beg_pos));
     if(tmp!="")
	  l_str.push_back(tmp);
	 tmp.clear();
	 
     //Получение начала следующего слова
     beg_pos=m_str[i].find_first_not_of(delims,end_pos);
   }
   if(choose_pos!=std::string::npos){
    if(m_str[i][choose_pos]=='|')
     l_str.push_back("|");
	//////////////////////////////
	/*if(m_str[i][delim_pos]=='[')
     l_str.push_back("[");
	if(m_str[i][delim_pos]=='{')
     l_str.push_back("{");
	if(m_str[i][delim_pos]=='|')
     l_str.push_back("/");*/
	//////////////////////////////
	//Сюда можно добавить код на другие символы
	// ....
   }
   ml_str.push_back(l_str);
   l_str.clear();
  }
  
  ////////////////////Удаление "дублей" (когда к примеру "Подлежащее" и "Дополнение", справа по сути одно и тоже)
  for(i=0; i<ml_str.size()-1; i++)
   for(j=i+1; j<ml_str.size(); j++){
    t=0;
    if(ml_str[i].size()==ml_str[j].size()){
     for(k=1; k<ml_str[i].size(); ++k)
      if(ml_str[i][k]!=ml_str[j][k]){
	   t=1;
	   break;
	  }
	 if(t==1) continue;
	 else{
	  for(l1=0; l1<ml_str.size(); ++l1)
       if(l1!=j)
		for(l2=1; l2<ml_str[l1].size(); ++l2)
		 if(ml_str[j][0]==ml_str[l1][l2])
		  ml_str[l1][l2]=ml_str[i][0];
	  count.push_back(j);
	  continue;
	 }
	}
   }
  for(i=0; i<count.size(); ++i)
   ml_str.erase(ml_str.begin()+count[i]-i);
  return ml_str;
 }
 
 std::vector<std::vector<std::string> > ReadFileEx(std::string FilePath){ 
  int i;
  std::string str;  
  std::vector<std::string> m_str;                //Вектор для считывания построчно с файла
  std::vector<std::string> l_str;                //Временный вектор для одной строки 
  std::vector<std::vector<std::string> > ml_str; //Вектор результата
  
  //////////////////Получение грамматики с файла//////////////////////
  std::ifstream fin(FilePath.c_str());    
  if(!fin){
   std::cout<<"File error!"<<std::endl;
   std::exit(0);
  }
  while(getline(fin,str)) 
    m_str.push_back(str);
  fin.close();
  
  /////////////////Выделение слов////////////////////
  std::string::size_type end_pos;
  std::string::size_type beg_pos;
  std::string tmp;                                                     //Для подстроки
  /////////////////Деление на слова
  for(i=0; i<m_str.size(); ++i){
   beg_pos=m_str[i].find_first_not_of(" ");
   while (beg_pos!=std::string::npos){
     //Определение конца слова
     end_pos=m_str[i].find_first_of(" ",beg_pos);
	 
     //Запись слова
     tmp.insert(0,m_str[i].substr(beg_pos, end_pos == std::string::npos // ?? end_pos ???"not found"
	                                 ? std::string::npos                // ???"all remaining characters"
                                     : end_pos - beg_pos));
     if(tmp!="")
	  l_str.push_back(tmp);
	 tmp.clear();
	 
     //Получение начала следующего слова
     beg_pos=m_str[i].find_first_not_of(" ",end_pos);
   }
   ml_str.push_back(l_str);
   l_str.clear();
  }
  return ml_str;
 }
 
 
 
 std::string Create(std::vector<std::vector<std::string> > one){
  int i,j,r,k,tmps,size=one.size();
  std::vector<std::string> one_tmp;
  std::vector<std::string>::iterator it;
  std::string result;
  
  //Нахождение главного терминала
  for(j=0; j<size; ++j){
   r=0;
   for(i=0; i<size; ++i){
    if(i!=j){
	 it=find(one[i].begin()+1,one[i].end(),one[j][0]);     //Если находит слово, то прерывает цикл
     if(it!=one[i].end()){
	  r=1;
	  break;
     }
	}  	
   }
   if(r==1) continue;                                //Продолжает дальше
   else if(r==0){                                    //Если находит, то заканчивает работу
	for(i=1; i<one[j].size(); ++i)
	 one_tmp.push_back(one[j][i]);                   //Копирует последовательность, принадлежащую главному терминалу
	break;
   }
  }
  
  //Получение рандомного предложения
  while(r!=1){
   for(j=0; j<one_tmp.size(); ++j){                         //Каждый раз образует новую строчку, расхлопывая предыдущую
	for(i=0; i<size; ++i){
	 tmps=one[i].size();
	 if(one_tmp[j]==one[i][0] && one[i][tmps-1]!="|"){             //Если нет выбора
	  one_tmp.erase(one_tmp.begin()+j);
	  for(k=1; k<tmps; ++k){
       one_tmp.insert(one_tmp.begin()+j+k-1,one[i][k]);
	  }
	  break;
	 }
     if(one_tmp[j]==one[i][0] && one[i][tmps-1]=="|"){             //Если есть выбор. Цикл рандома, не повторяющий вхождения
	  k=rand()%((int)(tmps-1));
      it=find(one_tmp.begin(),one_tmp.end(),one[i][k]); 	  
	  while(it!=one_tmp.end()){
	   k=rand()%((int)(tmps-1));
	   it=find(one_tmp.begin(),one_tmp.end(),one[i][k]); 
	  }
	  one_tmp.erase(one_tmp.begin()+j);
	  one_tmp.insert(one_tmp.begin()+j,one[i][k]);
	  break;
	 }
     //Можно вставить условия для других выборов	 
	 //...
	}
   }
   if(r!=one_tmp.size())
    r=one_tmp.size();
   else
    r=1;
  }
  
  for(i=0; i<one_tmp.size(); ++i)                          //Готовый результат
   result+=one_tmp[i]+" ";
  return result;
 }
 
 bool Destruct(std::vector<std::vector<std::string> > one, std::vector<std::string> two){
  int i,j,r,k,tmps,choose,size=one.size();
  std::vector<std::string> one_tmp=two;
  std::vector<std::string>::iterator it;
  std::vector<int> count;
  std::string result;
  
  //Нахождение главного терминала
  for(j=0; j<size; ++j){
   r=0;
   for(i=0; i<size; ++i){
    if(i!=j){
	 it=find(one[i].begin()+1,one[i].end(),one[j][0]);     //Если находит слово, то прерывает цикл
     if(it!=one[i].end()){
	  r=1;
	  break;
     }
	}  	
   }
   if(r==1) continue;                                //Продолжает дальше
   else if(r==0){                                    //Если находит, то заканчивает работу
	result=one[j][0];                                //Результатом должен быть главный терминал
	break; 
   }
  }
  
  //Попытка схлопнуть предложение
  while(one_tmp[0]!=result){
   r=0;
   for(j=0; j<one_tmp.size(); ++j){                         //Каждый раз образует новую строчку, схлопывая предыдущую
    count.clear();                                          //Очищаем массив
	for(i=0; i<size; ++i){
	 tmps=one[i].size();
	 it=find(one[i].begin()+1,one[i].end(),one_tmp[j]);
	 if(it!=one[i].end() && one[i][1]==one_tmp[j] && one[i][tmps-1]!="|"){             //Если нет выбора (записываем порядковые номера левых терминалов, если справа похоже на выбранную последовательность в примере предложения)
	  count.push_back(i);
	 }
     if(it!=one[i].end() && one[i][tmps-1]=="|"){             //Если есть выбор
	  one_tmp[j]=one[i][0];
	  r=1;
	  break;
	 }
     //Можно вставить условия для других выборов	 
	 //...
	}
	
	//Конфликтное множество схожих терминалов (например когда Прилагательное Существительное - Прилагательное - Прилагательное Глагол и т.п., первый терминал похож)
	while(count.size()!=0){
	 choose=count[0];
	 k=0;
	 for(i=1; i<count.size(); ++i)                    //Выбираем наибольшее по размеру из множества вошедших левых терминалов
	  if(one[count[i]].size()>=one[choose].size()){
       choose=count[i];
       k=i;	   
      }
	 count.erase(count.begin()+k);                    //Удаляем уже выбранный
	 tmps=one[choose].size();
     if(tmps!=2 && (one_tmp.size()-j)>=tmps-1){       //Для каждого выбранного таким образом терминала для предполагаемой свёртки, если справа больше 1 терминала, и предложение не заканчивается 
	  for(i=1; i<tmps; ++i){
	   if(one_tmp[j+i-1]!=one[choose][i]){
	    r=0;
	    break;
	   }
	   else r=1;
	  }
	  if(r==0) continue;                             //Если не получилось, снова выбираем элемент из конфликтного множества
	  one_tmp.erase(one_tmp.begin()+j, one_tmp.begin()+j+tmps-1); //Иначе свёртываем
	  one_tmp.insert(one_tmp.begin()+j, one[choose][0]);
	  break;
	 }
	 if(tmps==2){                                   //Если 1 терминал
	  one_tmp[j]=one[choose][0];                    //Заменяем на левый терминал
	  r=1;
	  break;
	 }
    }
   }
   if(r!=1)                                        //!=1 Если уже нечего свёртывать
    break;
  }
   
   
  //Если схлопнулось
  if(result==one_tmp[0])
   return true;
  
  //Если не вышло схлопнуть
  else if(result!=one_tmp[0])
   return false;
 }
 
