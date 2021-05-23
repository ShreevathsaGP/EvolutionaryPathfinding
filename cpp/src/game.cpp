#include <iostream>
#include <string>
#include <time.h>
#include <utility>
#include "SDL2/SDL.h"
#include "game.h"

using namespace std;

// dpd -> constructor() [ default ]
DPD::DPD() {  }

// dpd -> constructor() [ explicit ]
DPD::DPD(float probabilities_in[], int size) {
    distribution_size = size;
    probabilities = new float[size];
    for (int i = 0; i < size; i++) {
        probabilities[i] = probabilities_in[i];
    }
}

// dpd -> get_sample()
void DPD::get_sample(int sample[], int sample_size, int indices[]) {
    // make array pair
    pair<float, int> sorting_pair[distribution_size];
    for (int i = 0; i < distribution_size; i++) {
        sorting_pair[i].first = probabilities[i];
        sorting_pair[i].second = indices[i];
    }

    // sort array pair
    sort(sorting_pair, sorting_pair + distribution_size);
    for (int i = 0; i < distribution_size; i++) {
        probabilities[i] = sorting_pair[i].first;
        indices[i] = sorting_pair[i].second;
    }

    // updated info
    cout << "probs: ";
    print_array(probabilities, distribution_size);
    cout << "indices: ";
    print_array(indices, distribution_size);

    for (int i = 0; i < sample_size; i++) {
        // get random probability
        srand((unsigned)time(NULL));
        random_probability = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX));

        // base cases(1, 2)
        if (random_probability <= probabilities[0]) { sample[i] = 0; continue; }
        if (random_probability >= probabilities[distribution_size - 1]) { sample[i] = distribution_size - 1; continue; }

        // modified linear search
        for (int j = 0; j < distribution_size; j++) {
            if (probabilities[j] > random_probability) { sample[i] = j; break; }
        }
    }
    cout << "sample: ";
    print_array(sample, sample_size);
}

// dpd -> update_probabilities()
void DPD::update_probabilities(float probabilities_in[], int size) {
    distribution_size = size;
    probabilities = new float[size];
    for (int i = 0; i < size; i++) {
        probabilities[i] = probabilities_in[i];
    }
}

// game -> constructor()
Game::Game(unsigned int *total_frames_in, SDL_Renderer *renderer_in) {
    // car measurements
    car_height = height_car;
    car_width = height_car;

    // user car
    car_origin_x = 10;
    car_origin_y = (window_height / 2) - (car_height / 2);
    car_rect.x = car_origin_x;
    car_rect.y = car_origin_y;
    car_rect.w = car_width;
    car_rect.h = car_height;
    velocity = car_vel;

    // car population
    for (int i = 0; i < population_size; i++) {
        cars[i].x = car_origin_x;
        cars[i].y = car_origin_y;
        cars[i].w = car_width;
        cars[i].h = car_height;
    }

    // setup obstacles
    no_obstacles = 0;

    // SDL handling
    total_frames = total_frames_in;
    renderer = renderer_in;

    // temporary
    temp = false;
}

// game -> execute_instructions() [ population ]
void Game::execute_instructions(int instructions[population_size][dna_length], int status[population_size][3]) {
    // iterate dna units
    for (int j = 0; j < dna_length; j++) {
        // check if all dead
        temp = true;
        for (int i = 0; i < population_size; i++) {
            if (status[i][index::dead] == (int)false && status[i][index::reached] == (int)false) { temp = false; }
        }
        if (temp) { break; }

        // iterate population
        for (int i = 0; i < population_size; i++) {
            if (status[i][index::dead] == (int)false && status[i][index::reached] == (int)false) {
                switch(instructions[i][j]) {
                    case directions::up:
                        cars[i].y -= velocity;
                        break;
                    case directions::down:
                        cars[i].y += velocity;
                        break;
                    case directions::left:
                        cars[i].x -= velocity;
                        break;
                    case directions::right:
                        cars[i].x += velocity;
                        break;
                } 
                status[i][index::distance] = get_distance(i);
                if ((cars[i].x + (car_width / 2)) >= window_width) { status[i][index::reached] = (int)true; }
                if (cars[i].x < 0 || cars[i].y < 0 || (cars[i].y + car_height) > window_height) {
                    status[i][index::dead] = (int)true;
                }
            }
        }
        render_game();
    }
    reset_game();
}

// game -> execute_instructions() [ individual ]
void Game::execute_instructions(int instruction) {
    switch(instruction) {
        case directions::up:
            car_rect.y -= velocity;
            break;
        case directions::down:
            car_rect.y += velocity;
            break;
        case directions::left:
            car_rect.x -= velocity;
            break;
        case directions::right:
            car_rect.x += velocity;
            break;
    } 

    if (car_rect.x < 0 || car_rect.y < 0 || (car_rect.y + car_height) > window_height) {
        reset_game();
        return;
    }
}

// game -> reset_game()
void Game::reset_game() {
    for (int i = 0; i < population_size; i++) {
        cars[i].x = car_origin_x;
        cars[i].y = car_origin_y;
    }
    car_rect.x = car_origin_x;
    car_rect.y = car_origin_y;
}

// game -> render_game()
void Game::render_game() {
    // reset the widow completely
    SDL_SetRenderDrawColor(renderer, 0x0, 0x0, 0x0, 0xFF);
    SDL_RenderClear(renderer);

    // render user car
    SDL_SetRenderDrawColor(renderer, 11, 202, 212, 0xFF);
    SDL_RenderFillRect(renderer, &car_rect);

    // car population
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 0xFF);
    for (int i = 0; i < population_size; i++) {
        SDL_RenderFillRect(renderer, &cars[i]);
    }

    // render obstacles
    if (no_obstacles == 0) {}

    // correct for [fps = 30]
    frame_time = SDL_GetTicks() - frame_start;
    if (frame_delay > frame_time) { SDL_Delay(frame_delay - frame_time); }
    *total_frames = *total_frames + 1;

    // present the back buffer
    SDL_RenderPresent(renderer);
}

// game -> get_distance()
int Game::get_distance(int index) {
    return cars[index].x;
}

// game -> set_frame_start()
void Game::set_frame_start(Uint32 ticks) {
    frame_start = ticks;
}

// game -> get_random_value()
int get_random_value(int min, int max) {
    static bool first = true;
    if (first) {
      srand( time(NULL) ); //seeding for the first time only!
      first = false;
    }
    return min + rand() % (( max + 1 ) - min);
}

// print_array() [ int ]
void print_array(int array[], int size) {
    cout << "[ ";
    for (int i = 0; i < size; i++) {
        cout << array[i] << " ";
    }
    cout << "]" << endl;
}

// print_array() [ float ]
void print_array(float array[], int size) {
    cout << "[ ";
    for (int i = 0; i < size; i++) {
        cout << array[i] << " ";
    }
    cout << "]" << endl;
}

