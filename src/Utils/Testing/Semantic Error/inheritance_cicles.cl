class B inherits A
{
  b:String<-"cool";
  c:Int<-{2; 3;7+3;};
  sum(p1:Int,p2:Int):Int{ p1+p2 };
};
class A inherits C
{
   sum(p1:Int,p2:Int):Int{ p1+p2+9 };
};
class C inherits B
{
};
class Main
{
   main():Int{
       5
      
   };
};