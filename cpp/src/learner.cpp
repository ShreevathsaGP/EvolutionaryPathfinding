#include <iostream>
#include <string>
#include "SDL2/SDL.h"
#include "learner.h"
#include "game.h"

using namespace std;

// game -> constructor()
GA::GA(Game *game_in) {
    // randomize population
    for (int i = 0; i < population_size; i++) {
        for (int j = 0; j < dna_length; j++) {
            population[i][j] = get_random_value(dna_min, dna_max);
        }
    }

    // minimum fitness
    for (int i = 0; i < population_size; i++) {
        population_fitness[i] = min_fitness;
    }

    game = game_in;
}

// game -> update_fitness()
void GA::update_fitness() {
    // reset population status
    for (int i = 0; i < population_size; i++) {
        population_status[i][index::dead] = (int)false;
        population_status[i][index::reached] = (int)false;
        population_status[i][index::distance] = origin_car_x;
    }

    // execute dnas
    game -> execute_instructions(population, population_status);
    total_fitness = 0;
    
    // decide fitnesses
    for (int i = 0; i < population_size; i++) {
        population_fitness[i] = min_fitness;
        population_fitness[i] += population_status[i][index::distance];
        cout << "[ ";
        if (population_status[i][index::reached] == (int)true) { 
            population_fitness[i] += reached_bonus;
            cout << "reached | ";
        } else {
            cout << "noreach | ";
        }
        if (population_status[i][index::dead] == (int)false) {
            population_fitness[i] += alive_bonus;
            cout << "alive | ";
        } else {
            cout << "deded | ";
        }
        cout << population_fitness[i] << " ]" << endl;
        total_fitness += population_fitness[i];
    }

}

// game -> natural_selection()
void GA::natural_selection() {
    update_fitness(); 

    // reset population indices
    for (int i = 0; i < population_size; i++) {
        population_indices[i] = i;
    }
    
    // make probabilities
    for (int i = 0; i < population_size; i++) {
        population_fitness[i] /= total_fitness;
    }

    // get sample from discrete distribution
    distribution.update_probabilities(population_fitness, population_size);
    distribution.get_sample(distribution_sample, distribution_sample_size, population_indices);

    // introduce new population
    for (int i = 0; i < population_size; i++) {
        for (int j = 0; j < dna_length; j++) {
            new_population[i][j] = population[distribution_sample[i]][j];
        }
    }
}

// game -> crossover()
void GA::crossover(int parent[dna_length]) {
    random_float = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX));
    if (random_float < crossover_rate) {
        random_int = get_random_value(0, population_size); 
        // crossover at points
        for (int i = 0; i < dna_length; i++) {
            parent[i] = new_population[random_int][i];
        }
    }
}

// game -> mutation()
void GA::mutation(int child[dna_length]) {
    for (int i = 0; i < dna_length; i++) {
        random_float = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX));
        if (random_float < mutation_rate) {
            child[i] = get_random_value(directions::up, directions::right); // random direction
        }
    }
}

// game -> evolution_step()
void GA::evolution_step() {
    natural_selection();

    // for each parent
    for (int i = 0; i < population_size; i++) {
        // crossover for child
        crossover(new_population[i]);  

        // mutate child
        mutation(new_population[i]);
    }

    // population = new_population
    for (int i = 0; i < population_size; i++) {
        for (int j = 0; j < dna_length; j++) {
            population[i][j] = new_population[i][j];
        }
    }
}

