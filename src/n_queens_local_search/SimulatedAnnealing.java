package n_queens_local_search;

import java.util.Random;

public class SimulatedAnnealing implements Runnable {
	// attrs
	private int iterationLimit = 2000000000; // 2b
	private State initialState;
	private State bestState;
	private int bestEnergy = Integer.MAX_VALUE;

	private Thread thread;

	// get and set
	public State getInitialState() { return initialState; }
	public State getBestState() {
		return bestState;
	}

	// static
	private static Random random = new Random();

	// constructors
	public SimulatedAnnealing(State initialState) {
		this.bestState = initialState;
		this.initialState = initialState;
	}

	public SimulatedAnnealing() {
		this(GameState.randomState(8));
	}

	// methods
	/**
	 * pseudo code func:
	 * for k in [1, inf]:
	 *   T := tempSchedule[k]
	 *   if T = 0: return current
	 *   next := neighbor(current) # randomly selected
	 *   deltaEnergy := energy(next) - energy(current)
	 *
	 *   if deltaEnergy > 0: current := next
	 *   else if e^(deltaEnergy / T) >= random(0, 1):
	 *     current := next
	 *
	 * return current
	 */
	public State simulatedAnnealing() {
		State current = initialState;
		bestEnergy = current.energy();

		System.out.println("simulatedAnnealing simulated annealing\n" + initialState.toString());

		iterationLimit = 1000000; // 50m
		for (int iteration = 0; iteration < iterationLimit; ++iteration) {
			float temperature = initialState.temperatureScheduling(iteration);

			int currentEnergy = current.energy();
//			if (temperature == 0f || currentEnergy == -Integer.MAX_VALUE) return current;
			if (temperature == 0f || currentEnergy == -Integer.MAX_VALUE) bestState = current;

			State next = current.getRandomNeighbor();
			int nextEnergy = next.energy();
			if (nextEnergy < bestEnergy) {
				bestState = next;
				bestEnergy = nextEnergy;
			}

			int deltaEnergy = nextEnergy - currentEnergy;

			// sigmoid function to allow domain (-inf, inf) and range (0, 1)
			float deltaE = (deltaEnergy > 0 ? -1 : 1) * deltaEnergy;
			deltaE = deltaE == 0 ? -15 : deltaE;
			float probability = (float)(1 / (1 + Math.exp(deltaE / temperature))); // sigmoid: 1 / (1 + e^-x)

			if (nextEnergy < currentEnergy) current = next;
			else if (probability >= random.nextFloat()) {
				current = next;
			}

//			if (iteration % 500000 == 0 || iteration == iterationLimit - 1) {
			if (currentEnergy == -Integer.MAX_VALUE || iteration == iterationLimit - 1) {
				System.out.println("---------------------------------");
				System.out.println("deltaE: " + deltaEnergy);
				System.out.println("curntE: " + currentEnergy);
				System.out.println("currnt: " + current);
				System.out.println("next  : " + next);
				System.out.println("probab: " + probability);
				System.out.println("step  : " + iteration);

				return bestState;
			}
		}

		System.out.println(bestEnergy);
		return bestState;
	}

	public void start() {
		if (thread == null) {
			thread = new Thread(this, initialState.toString());
			thread.start();
		}
	}

	@Override
	public void run() {
		bestState = simulatedAnnealing();
	}
}
