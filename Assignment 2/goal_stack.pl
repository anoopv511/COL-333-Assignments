% Dynamic Predicate Declaration

:- dynamic on/2.	% on(A,B) - A is on B
:- dynamic ont/1.	% ont(A) - A is on table
:- dynamic cl/1.	% cl(A) - A has clear top
:- dynamic hold/1.	% hold(A) - Robot arm is holding A
:- dynamic ae/0.	% ae - Robot arm is empty
/*---------------------------------------------*/

% Helper Predicates

% Predicate to Read Initial State from File
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
	
% Predicate to print current state
printState :-
	listing(on),
	listing(ont),
	listing(cl),
	listing(ae),
	listing(hold).
/*---------------------------------------------*/	

% Action Predicates

% Stack A on B
s(A,B) :-
	achieve(cl(B)),
	achieve(hold(A)),
	retract(cl(B)),
	retract(hold(A)),
	assert(ae),
	assert(on(A,B)),
	write('Stacking '),write(A),write(' on '),writeln(B).

% Unstack A from B
us(A,B) :-
	achieve(on(A,B)),
	achieve(cl(A)),
	achieve(ae),
	retract(on(A,B)),
	retract(ae),
	assert(hold(A)),
	assert(cl(B)),
	write('Unstacking '),write(A),write(' from '),writeln(B).

% Pull up A
pu(A) :-
	achieve(ont(A)),
	achieve(cl(A)),
	achieve(ae),
	retract(ont(A)),
	retract(ae),
	assert(hold(A)),
	write('Pull up '),writeln(A).

% Put down A
pd(A) :-
	achieve(hold(A)),
	retract(hold(A)),
	assert(ont(A)),
	assert(ae),
	write('Put down '),writeln(A).
/*---------------------------------------------*/

% Predicates to validate Goals List

% Predicate to check the consistency of two list of predicates
validstate([], _).
validstate([A|R], L) :- valid(A, L), validstate(R, L).

% Predicate to check the consistency of a predicate wrt a list of predicates 
valid(_, []).

valid(on(A,B), [on(A,C)|_]) :- not(B= C), !, fail. 
valid(on(A,B), [on(B,A)|_]) :- !, fail.
valid(on(A,_), [ont(A)|_]) :- !, fail.
valid(on(_,B), [cl(B)|_]) :- !, fail.
valid(on(A,_), [hold(A)|_]) :- !, fail.
valid(on(_,B), [hold(B)|_]) :- !, fail.
valid(on(A,B), [_| L]) :- valid(on(A, B), L).

valid(ont(A), [hold(A)|_]) :- !, fail.
valid(ont(A), [_| L]) :- valid(ont(A), L).

valid(hold(_), [ae|_]) :- !, fail.
valid(hold(A), [_|L]) :- valid(hold(A), L).

valid(cl(_), _).

valid(ae, _).
/*---------------------------------------------*/

% Predicates to make plan for given Goals List

% Predicate to work out plan for achieving given Goal Stack
do(GoalStack) :- 
	validstate(GoalStack,GoalStack),
	writeln('Valid'),
	do_goals(GoalStack,GoalStack).

% Predicate to check if a goal is alread true
do_goals([G|R],Goals) :-
	call(G),
	do_goals(R,Goals),!.

% Predicate to achieve a goal from the List of Goals
do_goals([G|_],Goals) :-
	achieve(G),
	do_goals(Goals,Goals).

% Goals Finished (Base Case)
do_goals([],_Goals).
/*---------------------------------------------*/

% Predicates to achieve goals

% Achieve Predicate on(A,B)
achieve(on(A,B)) :-
	on(A,B), !.
achieve(on(A,B)) :-
	s(A,B).

% Achieve Predicate ont(A)
achieve(ont(A)) :-
	ont(A), !.
achieve(ont(A)) :-
	pd(A).

% Achieve Predicate hold(A)	
achieve(hold(A)) :-
	hold(A), !.
achieve(hold(A)) :-
	ont(A),
	pu(A), !.
achieve(hold(A)) :-
	us(A,_B).

% Achieve Predicate cl(A)	
achieve(cl(A)) :-
	cl(A), !.
achieve(cl(A)) :-
	us(_B,A).

% Achieve Predicate ae	
achieve(ae) :-
	ae, !.
achieve(ae) :-
	hold(X),
	pd(X), !.
/*---------------------------------------------*/