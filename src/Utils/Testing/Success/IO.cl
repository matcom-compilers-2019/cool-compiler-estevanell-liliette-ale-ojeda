class Main
{ 
    io:IO;
    x:String;
    y:String;
    z:String;
    main():Object
    {
        {
            x <- "Hello";
            y <- ", Good Morning";
            io.out_string((x.concat(y)).concat("!!!"));
            io.out_int(x.length());
            z <- y.substr(2,4);
            io.out_string(z.concat(" Day"));
            io.out_string(z.type_name());
        }
    };

};