#include<iostream>
using namespace std;
typedef struct BNode{
	char data;
	struct BNode *lchild,*rchild;
}BiTNode,*BiTree;

void CreateBiTree(BiTree &T,const char* values,int &i)
{
	if(values[i] == '#'){
		T = NULL;
		i++;
	}else{
		T = new BiTNode;
		T->data = values[i++];
		CreateBiTree(T->lchild, values, i);
		CreateBiTree(T->rchild,values,i);
	}
}

void PreOrderTraverse(BiTree T){
	if(T){
		cout<<T->data;          
		PreOrderTraverse(T->lchild); 
		PreOrderTraverse(T->rchild); 
	}
}

void InOrderTraverse(BiTree T){
	if(T){
		InOrderTraverse(T->lchild);
		cout<<T->data;
		InOrderTraverse(T->rchild);
	}
}

void PostOrderTraverse(BiTree T){
	if(T){
		PostOrderTraverse(T->lchild); 
		PostOrderTraverse(T->rchild); 
		cout<<T->data;               
	}
}

int main(){
	string input;  
    int i=0;
    BiTree tree;
    
    cout<<"请输入建立二叉链表的序列：\n";
    cout<<"示例：ABD##E##C#F##"<<endl;
    cin>>input; 
    
    CreateBiTree(tree,input.c_str(),i);  
    
    cout<<"先序遍历的结果为：";
    PreOrderTraverse(tree);
    cout<<endl;
    
    cout<<"中序遍历的结果为：";
    InOrderTraverse(tree);
    cout<<endl;
    
    cout<<"后序遍历的结果为：";
    PostOrderTraverse(tree);
    cout<<endl;
    
    return 0;
}

