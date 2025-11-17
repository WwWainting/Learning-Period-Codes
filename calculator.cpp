#include<iostream>
using namespace std;

const char oper[7] = {'+','-','*','/','(',')','#'};
#define OK 1
#define ERROR 0
#define OVERFLOW -2

typedef char SElemType;
typedef int Status;
typedef struct SNode{
	int data;
	struct SNode *next;
}SNode,*LinkStack;
/*初始化链栈*/
Status InitStack(LinkStack &S)
{
	S = NULL;
	return OK;
}
/*判断栈空*/
bool StackEmpty(LinkStack S)
{
	if(!S)
		return true;
	return false;
}
/*进栈*/
Status Push(LinkStack &S,SElemType e)
{
	SNode *p = new SNode;
	if(!p)
	{
		return OVERFLOW;
	}
	p->data = e;
	p->next = S;
	S = p;
	return OK;
}
/*出栈*/
Status Pop(LinkStack &S,SElemType &e)
{
	SNode *p;
	if(!S)
		return ERROR;
	e = S->data;
	p = S;
	S = S->next;
	delete p;
	return OK;
}
/*获取栈顶元素*/
Status GetTop(LinkStack &S,SElemType &e)
{
	if(!S)
		return ERROR;
	e = S->data;
	return OK;
}
/*判断是不是运算符*/
bool In(char ch)
{
	for(int i = 0;i < 7;i++){
		if(ch == oper[i])
		{
			return true;
		}
	}
	return false;
}
/*判断优先级*/
char Precede(char ch1,char ch2)
{
	if((ch1 == '('&&ch2 == ')') || (ch1 =='#' &&ch2 == '#') ){
		return '=';
	}
	else if(ch1 == '('||ch1 == '#'||ch2 == '('
		||(ch1 == '+'||ch1 == '-')&&(ch2 == '*'||ch2 == '/'))
	{
		return '<';
	}
	else
		return '>';
}
/*运算*/
char Operate(char first,char theta,char second){
	switch(theta){
		case '+':
			return (first - '0')+(second - '0')+ 48;
		case '-':
			return (first - '0')-(second - '0')+ 48;
		case '*':
			return (first - '0')*(second - '0')+ 48;
		case '/':
			return (first - '0')/(second - '0')+ 48; 
	}
	return 0;
}

int EvaluateExpression(){
	LinkStack OPTR,OPND;
	char theta,a,b,x,top;
	InitStack(OPTR);
	Push(OPTR,'#');
	InitStack(OPND);
	string str;
	cin>>str;
	string end;
	end = '#';
	str += end;
	int i = 0;
	char ch = str [0];
	while (ch != '#' || (GetTop(OPTR,top), top != '#')){
		if(!In(ch)){
			Push(OPND,ch);
			i++;
			ch = str[i];
		}
		else
			switch(GetTop(OPTR ,top),Precede(top,ch)){
				case '<':
					Push(OPTR,ch);
					i++;
					ch = str[i];
					break;
				case '>':
					Pop(OPTR,theta);
					Pop(OPND, b);
					Pop(OPND, a);
					Push(OPND,Operate(a,theta,b));
					break;
				case '=':
					Pop(OPTR, x);
					i++;
					ch=str[i];
					break;
			}
	}
	GetTop(OPND,ch);
	return ch;
}

int main()
{	
	cout << "请输入表达式: ";
	int res = EvaluateExpression();
	cout << "计算结果: " << res-48 << endl;
	return 0;
}