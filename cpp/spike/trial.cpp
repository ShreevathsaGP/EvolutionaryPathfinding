// discrete_distribution
#include <iostream>
#include <random>

using namespace std;

void print_array(int in_array[], int size);

class Something {
    public:
        Something(int in_array[2]) {
            free(array);
            array = new int[2];
            for (int i = 0; i < 2; i++) {
                array[i] = in_array[i];
            }
            print_array(array, 2);

        }

        void print() {
            print_array(array, 2);
        }
    private:
        int *array;
};

void print_array(int in_array[], int size) {
    cout << "[ ";
    for (int i = 0; i < size; i++) {
        cout << in_array[i] << " ";
    }
    cout << "]" << endl;
}
int main() {
    int nothing[2] = { 123, 123 };
    Something something = Something(nothing);
    nothing[0] = 0;
    nothing[1] = 0;

    something.print();
    
}
