#include <fstream>
#include <cstdio>
#include <string>
using namespace std;

int main(int argc, char* argv[]) {
    ifstream ifs(argv[1]);
    ofstream output;
    output.open(argv[2]);
    output << '[' << endl;
    string line;
    getline(ifs, line);
    output << line;
    int count = 1;
    while (getline(ifs, line)) {
        output << "," << endl;
        output << line;
        if (++count % 1000000 == 0) printf("%dth comments\n", count); 
    }
    output << endl;
    output << ']' << endl;
}
