class Main
{   
    main():Object
    {
        {
            (new IO).out_int(fib((new IO).in_int()));
        }
    };

    fib(x:Int):Int
    {
        if (x <= 2) then 1 else (fib(x-1) + fib(x-2)) fi
    };

};