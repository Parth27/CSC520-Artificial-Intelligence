relation("OED",isa,dictionary).

relation("Webster",isa,dictionary).

relation("Johnston",isa,dictionary).

relation("Flour water salt yeast",isa,cookbook).

relation("The Guide",isa,novel).

relation("Michael Strogoff",isa,fiction).

relation(novel,subset,fiction).

relation(dictionary,subset,nonfiction).

relation(cookbook,subset,nonfiction).

relation(fiction,subset,book).

relation(nonfiction,subset,book).

property(author,"Webster","Noah").

property(author,"Johnston","Samuel").

property(author,"Michael Strogoff","Jules").

property(author,"The Guide","RK").

property(20,volumeof,"OED").

relation("Webster",agreeswith,"Johnston").

relation("Johnston",agreeswith,"Webster").

relation("Johnston",agreeswith,"OED").

%Predicate to find volume of each book other than "OED"%

property(X,volumeof,Y):-
    relation(Y,isa,book),
    Y \= "OED",
    X=1.

%predicate to map each instance to their parents%

relation(X,isa,Y):-
    relation(Z,subset,Y),
    relation(X,isa,Z).

%Predicate for editor%

property(editor,X):-
    relation(X,isa,book).

%Predicate for hasauthor%

property(hasauthor,X):-
    relation(X,isa,fiction);
    property(author,X,_).


