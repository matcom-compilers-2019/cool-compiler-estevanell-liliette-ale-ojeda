class Main
{ 
    io:IO;
    x:Int <- 0;
    y:Int <- 0;
    main():Object
    {
        {
            y <- io.in_int();
            while x < y loop {
                x <- x+1;
                io.out_int(x);
                if x < y then io.out_string("-") else io.out_string("") fi;
            } pool;
        }
    };

};