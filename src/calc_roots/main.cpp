#include <iostream>
#include <cmath>
#include <iomanip>
#include "calculate_roots.h"
#include "bisection.h"
#include "newton_raphson.h"

using namespace std;

/**
 * Roots at x = {
 * 0.36509824,
 * 1.9217409,
 * 3.5631608}
 */
double functionA(double x) {
	return 2 * pow(x, 3.) - 11.7 * pow(x, 2.) + 17.7 * x - 5;
}

double fPrimeA(double x) {
    return 6 * pow(x, 2.) - 23.4 * x + 17.7;
}

/**
 * Root at x = 126.632
 */
double functionB(double x) {
	return x + 10 - x * cosh(50 / x);
}

int main() {
    CalculateRoots::functionOfX fA = &functionA;
    CalculateRoots::functionOfX fPA = &fPrimeA;

    // funcA, root1, bisection
	double guesses[] = {0., 0.5};
	Bisection bisection = Bisection(fA, guesses);
	vector<double> roots = bisection.calculateRoots();
	cout << setprecision(15) << roots.at(0) << endl;

	// funcA, root1, newton
	double guesses2[] = {0.5};
	NewtonRaphson newton = NewtonRaphson(fA, fPA, guesses2);
	roots = newton.calculateRoots();
	cout << setprecision(15) << roots.at(0) << endl;

	return 0;
}
