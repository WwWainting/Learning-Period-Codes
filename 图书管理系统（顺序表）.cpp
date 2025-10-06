#include<bits/stdc++.h>
#include<string>
using namespace std;

#define OK 1
#define ERROR 0

#define MAXSIZE 100
typedef struct Book{
	long id;
	string name;
	float price;
}Book,* Bookptr;
typedef Book ElemType;
typedef int Status;
/*顺序表实现*/
typedef struct LNode{
	ElemType *elem;
	int length;
}SqList;

void printmenu(){
	cout << "========== 图书管理系统 ==========" << endl;
    cout << "1. 查看一本图书的信息" << endl;
    cout << "2. 查看所有图书信息" << endl;
    cout << "3. 查找图书" << endl;
    cout << "4. 插入图书" << endl;
    cout << "5. 删除指定位置图书" << endl;
    cout << "6. 统计图书数量" << endl;
    cout << "7. 退出" << endl;
    cout << "===================================" << endl;
    cout << "请输入选择: ";
}

/*0*/
Status Init_SqList(SqList &L){
	L.elem = new ElemType[MAXSIZE];
	if(!L.elem) return ERROR;
	L.length = 0;
	return OK;
}

/*1*/
Status Get_elem(SqList L,int n,ElemType* e){
	//cout<<"请输入这本书的位置"<<endl;
	//cin>>n;
	if(n >L.length || n < 1) return ERROR;
	*e = L.elem[n-1];
	return OK;
}

/*2*/
void Show_Allelem(SqList L){
	for(int i = 0;i < L.length; i++){
		cout<<"编号："<<L.elem[i].id<<endl;
		cout<<"书名："<<L.elem[i].name<<endl;
		cout<<"价格："<<L.elem[i].price<<endl;
	}
}

/*3*/
Status Findelem_byname(SqList L ,string obj,ElemType *e){
	//cout<<"请输入这本书的名称"<<endl;
	//cin>>obj;
	int i;
	for(i = 0;i< L.length ;i++){
		if(L.elem[i].name == obj){
			*e = L.elem[i];
			return OK;
			}
	    }
	    if(i== L.length) return ERROR;
}

/*4*/
Status Insert_elem(SqList &L,int n,ElemType *e){
	if(n > L.length+1 || n < 1) return ERROR;
	//cout<<"请输入正确的位置"<<endl;
	for(int i = L.length-1;i >= n-1;i--){
		L.elem[i+1] = L.elem[i];
	}
	L.elem[n-1] = *e;
	L.length += 1;
	return OK;
}

/*5*/
Status Delete_elem(SqList &L,int n,ElemType &e){
	if(n >L.length || n< 1) return ERROR;
	e = L.elem[n-1];
	for(int i = n ;i < L.length;i++){
		L.elem[i-1] = L.elem [i];
	}
	L.length -= 1;
	return OK;
}

/*6*/
int Count_elem(SqList L){
	return L.length;
}

int main(){
	SqList L;
	ElemType e;
	int n;
	string obj;
	Init_SqList(L);
	int option;
	//测试数据
	L.elem[0].id = 10001; L.elem[0].name = "C++ Programming"; L.elem[0].price = 45.5; L.length++;
	L.elem[1].id = 10002; L.elem[1].name = "Data Structure"; L.elem[1].price = 39.8; L.length++;
	
	while(1)
	
	{
		printmenu();
		cin>>option;
		
		cin.ignore(1000, '\n');
		//清空缓冲区，防止留下东西后干扰正常使用
		
		switch(option){
			
			case 1:{
				cout<<"请输入这本书的位置"<<endl;
				cin>>n;
				
				if(Get_elem(L,n,&e)==1){
				cout<<"编号："<<e.id<<endl;
				cout<<"书名："<<e.name<<endl;
				cout<<"价格："<<e.price<<endl;
				cout<<"查找成功！"<<endl;
				}else
				cout<<"不存在这样的位置。"<<endl;
				break;
			}
			
			case 2:{
				Show_Allelem(L);
				break;
			}
			
			case 3:{
				cout<<"请输入这本书的名称"<<endl;
				//cin>>obj;无法兼容带空格的书名，会有东西留在缓冲区里面导致死循环
				getline(cin,obj);
				if(Findelem_byname(L,obj,&e)==1){
					cout<<"编号："<<e.id<<endl;
					cout<<"书名："<<e.name<<endl;
					cout<<"价格："<<e.price<<endl;
					cout<<"查找成功！"<<endl;
				}
				else cout<<"不存在这本书。"<<endl;
				break;
			}
			
			case 4:{
				cout<<"请输入要插入的位置:";
				cin>>n;
				cout<<"请输入要插入的元素"<<endl;
				cout<<"请输入要插入的元素"<<endl;
				cout<<"编号：";  
				cin>>e.id;
				cout<<"书名：";
				cin>>e.name;
				cout<<"价格：";
				cin>>e.price;
				if(Insert_elem(L,n,&e) == 1){
					cout<<"插入成功！"<<endl;
				}
				else cout<<"请输入正确的位置"<<endl;
				break;
			}
			
			case 5:{
				cout<<"请输入要删除的元素的位置：";
				cin>>n;
				ElemType temp;
				if(Delete_elem(L,n,temp)== 1){
					cout<<"删除成功！"<<endl;
				}else cout<<"请输入正确的位置"<<endl;
				break;
			}
			
			case 6:{
				cout<<"书架上总共有"<<Count_elem(L)<<"本书。"<<endl;
				break;
			}
			case 7:{
				exit(1);
				break;
			}
			default :{cout<<"输入有误，请重新输入！"<<endl;
				break;
			}
	}
}
	
	return 0;
}