#include <iostream>
#include <string>
#include "SDL2/SDL.h"
#include "learner.h"
#include "game.h"

using namespace std;

int main() {
    //--INITIALIZATIONS-----------------------------------------------------------------------------------------------
    // initialize SDL Components
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *window = SDL_CreateWindow("Flappy Reinforcements",0,0, window_width, window_height, SDL_WINDOW_SHOWN);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, 0);

    // initialize game variables
    unsigned int total_frames;
    GameData game_data;
    Game game = Game(&total_frames, renderer);
    GA genetic_algorithm = GA(&game);
    bool not_done = true;
    //--INITIALIZATIONS-----------------------------------------------------------------------------------------------
      
    //--SDL2----------------------------------------------------------------------------------------------------------
    bool learning = false;
    bool running = true;
    while (running) {
        // deal with [fps = 30]
        game.set_frame_start(SDL_GetTicks());

        // poll events
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            switch(event.type) {
                // x button
                case SDL_QUIT:
                    running = false;

                // keyboard
                case SDL_KEYDOWN:
                    switch(event.key.keysym.sym) {
                        // escape button
                        case SDLK_ESCAPE:
                            running = false;
                            break;
                        case SDLK_UP:
                           if (!learning) { game.execute_instructions(directions::up); }
                           break;
                        case SDLK_DOWN:
                           if (!learning) { game.execute_instructions(directions::down); }
                           break;
                        case SDLK_LEFT:
                           if (!learning) { game.execute_instructions(directions::left); }
                           break;
                        case SDLK_RIGHT:
                           if (!learning) { game.execute_instructions(directions::right); }
                           break;
                        default:
                           break;
                    }
            }
        }
    //--SDL2----------------------------------------------------------------------------------------------------------

    //--LEARNER-------------------------------------------------------------------------------------------------------
    
    genetic_algorithm.evolution_step();

    //--LEARNER-------------------------------------------------------------------------------------------------------

    //--RENDER--------------------------------------------------------------------------------------------------------
        // render game 
        game.render_game(); 
    //--RENDER--------------------------------------------------------------------------------------------------------
    }

    //--CLEANUP-------------------------------------------------------------------------------------------------------
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    //--CLEANUP-------------------------------------------------------------------------------------------------------

    return 0;
}
