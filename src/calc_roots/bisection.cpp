#include <iostream>
#include <iomanip>
#include "bisection.h"

using namespace std;

Bisection::Bisection(functionOfX f, double *guesses, int guessesSize, int maxIterations, double targetRelErr, double *trueRoot)
: BracketingMethod::BracketingMethod(f, guesses, guessesSize, maxIterations, targetRelErr, trueRoot) {
    methodName = "Bisection";
}

void Bisection::calculateApproximation() {
    // max iter or target rel. err. reached
    if (exitConditionsMet())
        return;

	previousApproximation = approximation;
	approximation = (x1 + x2) / 2;

	fapprox = f(approximation);
	printIteration();

	// root found, done iterating
	if (setupNextIteration()) {
        roots.push_back(approximation);
		return;
	}

	// update function values so they're calc once per iter
	fx1 = f(x1);
	fx2 = f(x2);

	iterations++;
	// recursive call
	calculateApproximation();
}

bool Bisection::setupNextIteration() {
	float signOfProduct = fx1 * fapprox;

	// root found - we're at zero or extremely close to it
	if (rootFound())
        return true;
	else if (signOfProduct < 0)
		x2 = approximation;
	else
		x1 = approximation;

	return false;
}

void Bisection::printIteration() {
    calculateErrors();
    double numbs[] = {(double)iterations, x1, x2, approximation, fx1, fx2, fapprox, absoluteError, relativeError};
    // print values in this row for this iteration of the table
    recordItems(numbs, sizeof(numbs)/sizeof(*numbs));
}

void Bisection::printIterationHeader() {
    string headers[] = {"n", "a", "b", "c", "f(a)", "f(b)", "f(c)", "Abs. Err.", "Rel. Err."};
    recordItems(headers, sizeof(headers)/sizeof(*headers));
    cout << endl;
}
