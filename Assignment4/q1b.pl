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

%predicate to map each instance to their parents%

relation(X,isa,Y):-
    relation(Z,subset,Y),
    relation(X,isa,Z).
