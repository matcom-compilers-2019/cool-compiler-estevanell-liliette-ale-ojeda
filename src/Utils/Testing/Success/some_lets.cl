class A
{
   sum(p1:Int,p2:Int):Int{ p1+p2+1};
};
class B inherits A
{
  a:Int<-{2; 3;7+3;};
  d:Int<-1;
  sum(p1:Int,p2:Int):Int{ let a:Int<-(1+3),b:Int<-0 in (let a:Int<-5,c:Int<-3 in a+b+c)+a+d};

};
class Main
{
    a:A<- new B;
    main():Int
    {
        a.sum(1,2)
    };
};