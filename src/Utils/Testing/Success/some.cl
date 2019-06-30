class Main
{   
    sum(x:Int):Int
    {
        x+10
    };
    main():Object
    {
        {
            (new IO).out_int((new C).sum(10));
            (new IO).out_string("     ");
            (new IO).out_int((new C).mult(2));
            (new IO).out_string("     ");
            (new IO).out_int((new C)@A.sum(4));
            (new IO).out_string("     ");
            (new IO).out_int(sum(1));
        }
    };
};
class A
{
    a:Int <- 10;
    sum(x:Int):Int{
        x+1
    };
};

class B inherits A
{
    sum(x:Int):Int{
        x+2
    };
    mult(x:Int):Int{
        x*a
    };
};
class C inherits B
{
    sum(x:Int):Int{
        x+3
    };
};