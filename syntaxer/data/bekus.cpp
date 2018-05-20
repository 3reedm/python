#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

/**

��ଠ �����-����. �ணࠬ��

//���⠢��� ᨭ⠪��᪨� ��������� ��� �ࠬ��⨪�, ��宦�� �� ���:

<����⢨⥫쭮�>::=���|�������|���
<�ਫ���⥫쭮�>::=����|��஬��|���񪨩
<������>::=���|��������|��

<����㥬��>::=<������>
<�������饥>::=<�ਫ���⥫쭮�> <����⢨⥫쭮�>
<����������>::=<�ਫ���⥫쭮�> <����⢨⥫쭮�>

<�।�������>::=<�������饥> <����㥬��> <����������>

**/

 std::vector<std::vector<std::string> > ReadFileGram(std::string);
 std::vector<std::vector<std::string> > ReadFileEx(std::string);
 std::string Create(std::vector<std::vector<std::string> >);
 bool Destruct(std::vector<std::vector<std::string> >, std::vector<std::string>);
 
int main(){
 int i,j;
 std::vector<std::vector<std::string> > gram;
 std::vector<std::vector<std::string> > examples;
 gram=ReadFileGram("gram.txt");                      //���뢠��� �ࠬ��⨪�
 examples=ReadFileEx("examples.txt");                //���뢠��� �ਬ�஢ �।�������
 
 //��� �����஢���� �।�������, �ᯮ���� �ࠬ��⨪�
 //���� ��� ����
 std::cout<<std::endl<<"-----------------------------����஥��� �।�������-----------------------------"<<std::endl;                            
 for(i=0; i<5; ++i){                    
  std::cout<<i+1<<". "<<Create(gram)<<std::endl;
 }
 
 //��� �஢�ન �� �ਭ���������� �ࠬ��⨪�  
 //���� ��� ����
 std::cout<<std::endl<<"---------------------�஢�ઠ �� �ਭ���������� �ࠬ��⨪�----------------------"<<std::endl;
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
   std::cout<<" �ਭ������� �ࠬ��⨪�"<<std::endl;
  else
   std::cout<<" �� �ਭ������� �ࠬ��⨪�"<<std::endl;
 }
 
 return 0;
}

 
 std::vector<std::vector<std::string> > ReadFileGram(std::string FilePath){ 
  int i,j,k,t,l1,l2;
  std::string str; 
  std::vector<int> count;  
  std::vector<std::string> m_str;                //����� ��� ���뢠��� �����筮 � 䠩��
  std::vector<std::string> l_str;                //�६���� ����� ��� ����� ��ப� 
  std::vector<std::vector<std::string> > ml_str; //����� १����
  
  //////////////////����祭�� �ࠬ��⨪� � 䠩��//////////////////////
  std::ifstream fin(FilePath.c_str());    
  if(!fin){
   std::cout<<"File error!"<<std::endl;
   std::exit(0);
  }
  while(getline(fin,str)) 
    m_str.push_back(str);
  fin.close();
  
  /////////////////�뤥����� ᫮�////////////////////
  std::string delims;                 /*" :=|<>"*/                            //��㦥��� ���ନ����� ᨬ���� "|" - ��� (or); "::=" - �⤥����� ����� ��� �� �ࠢ��; "<>" - � ᪮���� 㪠���� ��� �ந������ �ନ����; " " - � (and).
  const std::string choose("|");      /*"[{/|"*/                              //����� �������� ᨬ����, ����� ⮦� 㢥��稢��� ����������� �롮�, �����.
  std::string::size_type end_pos;
  std::string::size_type choose_pos;
  std::string::size_type beg_pos;
  std::string tmp;                                                     //��� �����ப�
  /////////////////������� �� ᫮��
  for(i=0; i<m_str.size(); ++i){
   delims=" :=|<>";
   choose_pos=m_str[i].find_first_of(choose);
   if(choose_pos!=std::string::npos)
    delims=":=|<>";
   beg_pos=m_str[i].find_first_not_of(delims);
   while (beg_pos!=std::string::npos){
     //��।������ ���� ᫮��
     end_pos=m_str[i].find_first_of(delims,beg_pos);
	 
     //������ ᫮��
     tmp.insert(0,m_str[i].substr(beg_pos, end_pos == std::string::npos // ?? end_pos ???"not found"
	                                 ? std::string::npos                // ???"all remaining characters"
                                     : end_pos - beg_pos));
     if(tmp!="")
	  l_str.push_back(tmp);
	 tmp.clear();
	 
     //����祭�� ��砫� ᫥���饣� ᫮��
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
	//� ����� �������� ��� �� ��㣨� ᨬ����
	// ....
   }
   ml_str.push_back(l_str);
   l_str.clear();
  }
  
  ////////////////////�������� "�㡫��" (����� � �ਬ��� "�������饥" � "����������", �ࠢ� �� ��� ���� � ⮦�)
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
  std::vector<std::string> m_str;                //����� ��� ���뢠��� �����筮 � 䠩��
  std::vector<std::string> l_str;                //�६���� ����� ��� ����� ��ப� 
  std::vector<std::vector<std::string> > ml_str; //����� १����
  
  //////////////////����祭�� �ࠬ��⨪� � 䠩��//////////////////////
  std::ifstream fin(FilePath.c_str());    
  if(!fin){
   std::cout<<"File error!"<<std::endl;
   std::exit(0);
  }
  while(getline(fin,str)) 
    m_str.push_back(str);
  fin.close();
  
  /////////////////�뤥����� ᫮�////////////////////
  std::string::size_type end_pos;
  std::string::size_type beg_pos;
  std::string tmp;                                                     //��� �����ப�
  /////////////////������� �� ᫮��
  for(i=0; i<m_str.size(); ++i){
   beg_pos=m_str[i].find_first_not_of(" ");
   while (beg_pos!=std::string::npos){
     //��।������ ���� ᫮��
     end_pos=m_str[i].find_first_of(" ",beg_pos);
	 
     //������ ᫮��
     tmp.insert(0,m_str[i].substr(beg_pos, end_pos == std::string::npos // ?? end_pos ???"not found"
	                                 ? std::string::npos                // ???"all remaining characters"
                                     : end_pos - beg_pos));
     if(tmp!="")
	  l_str.push_back(tmp);
	 tmp.clear();
	 
     //����祭�� ��砫� ᫥���饣� ᫮��
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
  
  //��宦����� �������� �ନ����
  for(j=0; j<size; ++j){
   r=0;
   for(i=0; i<size; ++i){
    if(i!=j){
	 it=find(one[i].begin()+1,one[i].end(),one[j][0]);     //�᫨ ��室�� ᫮��, � ���뢠�� 横�
     if(it!=one[i].end()){
	  r=1;
	  break;
     }
	}  	
   }
   if(r==1) continue;                                //�த������ �����
   else if(r==0){                                    //�᫨ ��室��, � �����稢��� ࠡ���
	for(i=1; i<one[j].size(); ++i)
	 one_tmp.push_back(one[j][i]);                   //������� ��᫥����⥫쭮���, �ਭ��������� �������� �ନ����
	break;
   }
  }
  
  //����祭�� ࠭������� �।�������
  while(r!=1){
   for(j=0; j<one_tmp.size(); ++j){                         //����� ࠧ ��ࠧ�� ����� �����, ��嫮�뢠� �।�����
	for(i=0; i<size; ++i){
	 tmps=one[i].size();
	 if(one_tmp[j]==one[i][0] && one[i][tmps-1]!="|"){             //�᫨ ��� �롮�
	  one_tmp.erase(one_tmp.begin()+j);
	  for(k=1; k<tmps; ++k){
       one_tmp.insert(one_tmp.begin()+j+k-1,one[i][k]);
	  }
	  break;
	 }
     if(one_tmp[j]==one[i][0] && one[i][tmps-1]=="|"){             //�᫨ ���� �롮�. ���� ࠭����, �� �������騩 �宦�����
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
     //����� ��⠢��� �᫮��� ��� ��㣨� �롮஢	 
	 //...
	}
   }
   if(r!=one_tmp.size())
    r=one_tmp.size();
   else
    r=1;
  }
  
  for(i=0; i<one_tmp.size(); ++i)                          //��⮢� १����
   result+=one_tmp[i]+" ";
  return result;
 }
 
 bool Destruct(std::vector<std::vector<std::string> > one, std::vector<std::string> two){
  int i,j,r,k,tmps,choose,size=one.size();
  std::vector<std::string> one_tmp=two;
  std::vector<std::string>::iterator it;
  std::vector<int> count;
  std::string result;
  
  //��宦����� �������� �ନ����
  for(j=0; j<size; ++j){
   r=0;
   for(i=0; i<size; ++i){
    if(i!=j){
	 it=find(one[i].begin()+1,one[i].end(),one[j][0]);     //�᫨ ��室�� ᫮��, � ���뢠�� 横�
     if(it!=one[i].end()){
	  r=1;
	  break;
     }
	}  	
   }
   if(r==1) continue;                                //�த������ �����
   else if(r==0){                                    //�᫨ ��室��, � �����稢��� ࠡ���
	result=one[j][0];                                //������⮬ ������ ���� ������ �ନ���
	break; 
   }
  }
  
  //����⪠ �嫮����� �।�������
  while(one_tmp[0]!=result){
   r=0;
   for(j=0; j<one_tmp.size(); ++j){                         //����� ࠧ ��ࠧ�� ����� �����, �嫮�뢠� �।�����
    count.clear();                                          //��頥� ���ᨢ
	for(i=0; i<size; ++i){
	 tmps=one[i].size();
	 it=find(one[i].begin()+1,one[i].end(),one_tmp[j]);
	 if(it!=one[i].end() && one[i][1]==one_tmp[j] && one[i][tmps-1]!="|"){             //�᫨ ��� �롮� (�����뢠�� ���浪��� ����� ����� �ନ�����, �᫨ �ࠢ� ��宦� �� ��࠭��� ��᫥����⥫쭮��� � �ਬ�� �।�������)
	  count.push_back(i);
	 }
     if(it!=one[i].end() && one[i][tmps-1]=="|"){             //�᫨ ���� �롮�
	  one_tmp[j]=one[i][0];
	  r=1;
	  break;
	 }
     //����� ��⠢��� �᫮��� ��� ��㣨� �롮஢	 
	 //...
	}
	
	//���䫨�⭮� ������⢮ �宦�� �ନ����� (���ਬ�� ����� �ਫ���⥫쭮� ����⢨⥫쭮� - �ਫ���⥫쭮� - �ਫ���⥫쭮� ������ � �.�., ���� �ନ��� ��宦)
	while(count.size()!=0){
	 choose=count[0];
	 k=0;
	 for(i=1; i<count.size(); ++i)                    //�롨ࠥ� �������襥 �� ࠧ���� �� ������⢠ ��襤�� ����� �ନ�����
	  if(one[count[i]].size()>=one[choose].size()){
       choose=count[i];
       k=i;	   
      }
	 count.erase(count.begin()+k);                    //����塞 㦥 ��࠭��
	 tmps=one[choose].size();
     if(tmps!=2 && (one_tmp.size()-j)>=tmps-1){       //��� ������� ��࠭���� ⠪�� ��ࠧ�� �ନ���� ��� �।���������� ���⪨, �᫨ �ࠢ� ����� 1 �ନ����, � �।������� �� �����稢����� 
	  for(i=1; i<tmps; ++i){
	   if(one_tmp[j+i-1]!=one[choose][i]){
	    r=0;
	    break;
	   }
	   else r=1;
	  }
	  if(r==0) continue;                             //�᫨ �� ����稫���, ᭮�� �롨ࠥ� ����� �� ���䫨�⭮�� ������⢠
	  one_tmp.erase(one_tmp.begin()+j, one_tmp.begin()+j+tmps-1); //���� ����뢠��
	  one_tmp.insert(one_tmp.begin()+j, one[choose][0]);
	  break;
	 }
	 if(tmps==2){                                   //�᫨ 1 �ନ���
	  one_tmp[j]=one[choose][0];                    //�����塞 �� ���� �ନ���
	  r=1;
	  break;
	 }
    }
   }
   if(r!=1)                                        //!=1 �᫨ 㦥 ��祣� ����뢠��
    break;
  }
   
   
  //�᫨ �嫮��㫮��
  if(result==one_tmp[0])
   return true;
  
  //�᫨ �� ��諮 �嫮�����
  else if(result!=one_tmp[0])
   return false;
 }
 
