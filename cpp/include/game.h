#ifndef GAME_H_
#define GAME_H_

#include "SDL2/SDL.h"

// window dimensions
const int window_height = 500;
const int window_width = 800;
const int height_car = (window_height / 18);
const int width_car = (window_width / 18);

// directions
enum directions {
    up = 0,
    down = 1,
    left = 2,
    right = 3
};

// car stuff
const int origin_car_x = 10;
const int origin_car_y = (window_height / 2) - (height_car / 2);
const int car_vel = 12;

// learning stuff
const int population_size = 100;
const int dna_length = 1e3;
const float crossover_rate = 6e-1; // [ crossover probability ]
const float mutation_rate = 5e-1; // [ mutation probability ]
const int no_generations = 1e2;
const int dna_min = directions::up;
const int dna_max = directions::right;
const float min_fitness = 1e-3 + width_car + (2 * car_vel);

// fitness bonuses
const int alive_bonus = window_width / 15;
const int reached_bonus = window_width / 5;

// indices
enum index {
    dead = 0,
    reached = 1,
    distance = 2
};

// fpd constants [fps = 30]
const int fps = 30;
const int frame_delay = 1000 / fps;

// game data
struct GameData {
    unsigned int generation;
    int fittest_index;
    int best_fitness;
};

// Discrete Probability Distribution
class DPD {
    public:
        // constructor() [ default ]
        DPD();  

        // constructor() [ explicit ]
        DPD(float probabilities_in[], int size);

        // get_sample()
        void get_sample(int sample[], int sample_size, int indices[]);

        // update_probabilities()
        void update_probabilities(float probabilities_in[], int size);

    private:
        // probability 
        float *probabilities;
        int *indices;
        float random_probability;
        int distribution_size;
};

// Game
class Game {
    public:
        // constructor()
        Game(unsigned int *total_frames_in, SDL_Renderer *renderer_in);

        // execute_instructions() [ population ]
        void execute_instructions(int instructions[population_size][dna_length], int status[population_size][3]);

        // execute_instructions() [ individual ]
        void execute_instructions(int instruction);
        
        // reset_game()
        void reset_game();

        // render_game()
        void render_game();

        // get_distance()
        int get_distance(int index);

        // set_frame_start()
        void set_frame_start(Uint32 ticks);
    
    private:
        // measurement 
        int car_height;
        int car_width;
        int temp_measurement;

        // position 
        int car_origin_x;
        int car_origin_y;
        short int velocity;

        // obstacle 
        int obstacles[10]; 
        int no_obstacles;

        // render 
        SDL_Rect car_rect;
        SDL_Rect cars[population_size];

        // SDL 
        Uint32 frame_start;
        unsigned int *total_frames;
        int frame_time;
        SDL_Renderer *renderer;

        // temperory 
        bool temp;
};

// get_random_value()
int get_random_value(int min, int max);

// print_array() [ int ]
void print_array(int array[], int size);

// print_array() [ float ]
void print_array(float array[], int size);

#endif // GAME_H_
