%Starts from first node and builds the list until the goal node appears%
criticalPath(TASK,[H|T]):-
    first(Y),
    H=Y,
    duration(Y,Z),
    createpath(TASK,Y,T,Z).

%Predicates used by critical path%

createpath(Original,TASK,[H|T],Time):-
    prerequisite(Next,TASK),
    duration(Next,Y),
    Time1 is Time+Y,
    H=Next,
    createpath(Original,Next,T,Time1).

createpath(Original,TASK,[],Time):-
    Original==TASK,
    duration(TASK,Y),
    \+(createpath(Original,Time,Y)).

createpath(TASK,Time2,Time):-
    prerequisite(TASK,PREV),
    duration(PREV,Y),
    Time1 is Time+Y,
    createpath(PREV,Time2,Time1).

createpath(TASK,Time2,Time):-
    \+(prerequisite(TASK,PREV)),
    Time2<Time.

%Predicate to find first node of graph%
first(X):-
    prerequisite(_,X),
    \+(prerequisite(X,_)).

%Predicate to find last node of graph%
last(X):-
    prerequisite(X,Y),
    \+(prerequisite(NEXT,X)).

earlyFinish(TASK,Time):-
    path(TASK,Time).

%Predicates used by early finish%
path(TASK,Time):-
    first(Y),
    duration(Y,Z),
    path(TASK,Y,Z,Time).

path(Original,TASK,Time,Time2):-
    Original==TASK,
    duration(TASK,Y),
    \+(createpath(Original,Time,Y)),
    Time=Time2.

path(Original,TASK,Time,Time2):-
    prerequisite(Next,TASK),
    duration(Next,Y),
    Time1 is Time+Y,
    path(Original,Next,Time1,Time2).

% Traverses from last node to calulate LS of each node until the goal%
% node appears%

lateStart(TASK,Time):-
    last(X),
    TASK==X,
    earlyFinish(X,Time1),
    duration(X,Y),
    Time is Time1-Y.

lateStart(TASK,Time):-
    last(X),
    earlyFinish(X,Time1),
    duration(X,Y),
    prerequisite(X,Z),
    LS is Time1-Y,
    ls(TASK,Z,LS,Time).

% Predicates to make sure that lowest LS is chosen in case of%
% multiple paths to a node, while traversing back from final node%

minLS(TASK,Time):-
    last(X),
    earlyFinish(X,Time1),
    duration(X,Y),
    prerequisite(X,Z),
    LS is Time1-Y,
    minLS(TASK,Z,LS,Time).

minLS(TASK,Current,LS,Time):-
    Current==TASK,
    duration(Current,T),
    Time2 is LS-T,
    Time2<Time.

minLS(TASK,Current,LS,Time):-
    duration(Current,T),
    LS1 is LS-T,
    prerequisite(Current,PREV),
    minLS(TASK,PREV,LS1,Time).

ls(TASK,Current,LS,Time):-
    Current=TASK,
    duration(Current,T),
    Time is LS-T,
    \+(minLS(TASK,Time)).

ls(TASK,Current,LS,Time):-
    duration(Current,T),
    LS1 is LS-T,
    prerequisite(Current,PREV),
    ls(TASK,PREV,LS1,Time).

maxSlack(TASK,Slack):-
    lateStart(TASK,Time),
    earlyFinish(TASK,Time1),
    duration(TASK,X),
    Time2 is Time1-X,
    Slack is Time-Time2,
    \+(slack(Slack)).

%To make sure that no other node has a larger slack%

slack(Slack):-
    lateStart(T,Time),
    earlyFinish(T,Time1),
    duration(T,X),
    Time2 is Time1-X,
    Slack1 is Time-Time2,
    Slack1>Slack.





















