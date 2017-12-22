:- dynamic frame/2.

readFile(InputFile) :- 
	seeing(OldStream),
	see(InputFile),
	repeat,
	read(Term),
	( Term == end_of_file -> true ; 
		writeln(Term), Term, fail
		),
		seen,
		see(OldStream).

search(_,[]).

search([Y|Xs],[Y|Ys]) :-
	search(Xs,Ys).

search([_|Xs],[Y|Ys]) :-
	search(Xs,[Y|Ys]).	

find(X,Y) :-
	frame(X,Z),
	search(Z,Y),!.

find(X,Y) :-
	frame(X,[inst(Z),_]),
	find(Z,Y),!.

find(X,Y) :-
	frame(X,[ako(Z),_]),
	find(Z,Y),!.

find(X,Y) :-
	frame(X,[a_part_of(Z),_]),
	find(Z,Y).