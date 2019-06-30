class Main{
   io:IO<- new IO;
     msg:String<-"Hello World";
     c:C<- new C;
     x:C<- new B;
     y:Int<-c.func();
     main():Int{
        {
           io.out_string(msg);
           io.out_string(" ");
           io.out_string(c.cool());
           io.out_string(" ");
           io.out_int(c@A.sum(1,2));
           io.out_string(" ");
           io.out_int((new B).sum(1,2));
           io.out_string(" ");
           io.out_int(c.sum(1,2));
        }
     };

};
class A
{
   sum(p1:Int,p2:Int):Int{ "hola"};
   mult(p1:Int,p2:Int):Int{ p1*p2 };
};
class B inherits A
{
  sum(p1:Int,p2:Int):Int{ mult(p1,p1)+mult(p2,p2)};
  cmp(x:Int,s:String):Bool{{x+s;x<s;}};
  error(x:Int,x:String):Bool{true};
  err():Int{if "cool" then 1 else 5 fi};
};
class C inherits B
{
   sum(p1:Int,p2:Int):Int{ (new C)@B.sum(p1,p2) + mult(1,true)};
   cool():String{type_name().concat("ool")};
};
