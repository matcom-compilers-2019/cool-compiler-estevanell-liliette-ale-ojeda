class A inherits B
{

};
class B
{

};
class C inherits B
{

};

class Main
{   
    main(): Object
    {
        case (new C) of
        x:A => (new IO).out_string((new A).type_name());
        x:B => (new IO).out_string((new B).type_name());
        x:C => (new IO).out_string((new C).type_name());
        esac        
    };    
};