#ifndef LEARNER_H_
#define LEARNER_H_

#include "SDL2/SDL.h" 
#include "game.h"

const int distribution_sample_size = population_size;

// Genetic Algorithm
class GA {
    public:
        // constructor()
        GA(Game *game_in);

        // update_fitness()
        void update_fitness();

        // natural_selection()
        void natural_selection();

        // crossover()
        void crossover(int parent[dna_length]);

        // mutation()
        void mutation(int child[dna_length]);

        // evolution_step()
        void evolution_step();

    private:
        // population 
        int population[population_size][dna_length];
        int population_indices[population_size];
        int new_population[population_size][dna_length];
        float population_fitness[population_size];
        int population_status[population_size][3]; // [ dead, reached, distance ]

        // fittess
        int fittest_index;
        float total_fitness;

        // game
        Game *game;

        // distribution
        DPD distribution;
        int distribution_sample[distribution_sample_size];
        float random_float; // [ 0 <= random_float <= 1 ]
        int random_int; // [0 <= random_int <= population_size]
};


#endif // LEARNER_H_
