package n_queens_local_search;

interface State {
	State getRandomNeighbor();
	float temperatureScheduling(int step);
	int energy();
	boolean isSolution();
}