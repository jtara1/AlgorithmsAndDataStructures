package n_queens_local_search;

interface State extends Comparable<State> {
	// get and set
	int getMaxFitness();

	// methods
	State getRandomNeighbor();
	float temperatureScheduling(int step);
	int energy();

	int fitness();
	State reproduce(State state_pointer);
	State mutate();

	boolean isSolution();

	int hashCode();
}
