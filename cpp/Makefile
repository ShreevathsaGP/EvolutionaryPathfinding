# REGULAR
play: main
	./bin/simulate

main: src/main.cpp learner
	g++ build/game.o build/learner.o src/main.cpp -o bin/simulate -I include -L lib -l SDL2-2.0.0 -l SDL2_ttf 

learner: src/learner.cpp game
	g++ -c src/learner.cpp -o build/learner.o -I include

game: src/game.cpp
	g++ -c src/game.cpp -o build/game.o -I include

trial: spike/trial.cpp
	g++ spike/trial.cpp -o bin/spike;
	./bin/spike
