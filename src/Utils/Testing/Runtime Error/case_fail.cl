class Main {
            attr1: A;
            main() : Int {
                {
                    case attr1 of
                        id1:A => let io: IO <- new IO in io.out_string("Es A");
                        id2:B => let io: IO <- new IO in io.out_string("Es B");
                    esac;
                   5;
               }
            };
        };
class A {};
class B inherits A {};