class A
{ 
   sum(p1:Int,p2:Int):Int{ p1+p2+1};
};
class B inherits A
{
  b:String<-"cool";
  c:Int<-{2; 7;};
  sum(p1:Int,p2:Int, p3:Int):Int{ p1+p2 };
  b:Int;

};

class D inherits IO
{
};
class Main
{
   main():Int{
       5  
   };
};