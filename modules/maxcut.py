import qiskit as qi
import numpy as np
import math
from matplotlib import pyplot as plt
import random
from scipy.optimize import minimize 
from qiskit.tools.visualization import plot_histogram

class MaxCut:
    """
    Description: a QAOA based MaxCut solver
    """
    def __init__(self, wgraph):
        """
        Args:
            wgraph: a weighted networkx Graph object
        """
        self.wgraph = wgraph
        self.num_qubits = len(wgraph)
        self.simulator = qi.Aer.get_backend('qasm_simulator')

    def int_to_bit_string(self, integer):
        """
        Description: turns an integer into a bit-string with self.num_qubits bits
        
        Args:
            integer: integer to be turned into a bit-string
        
        Returns: the computed bit-string
        """
        bit_string = bin(integer)[2:]
        # pad with appropriate number of 0's and return the bit-string
        return '0' * (self.num_qubits - len(bit_string)) + bit_string

    def classical_objective(self, bit_string):
        """
        Description: computes the classical objective function for max-cut (to be minimized)

        Arg: 
            bit_string: a bit-string defining the cut
        
        Returns: - 2 * sum of inter-cluster edge weights
        """
        cost = 0.0
        for (u, v) in self.wgraph.edges:
            cost += self.wgraph.edges[u, v]['weight'] * ((-1)**(int(bit_string[u]) + int(bit_string[v])) - 1)
        return cost

    def cost_operator(self, gamma):
        """
        Description: defines the cost operator e^(-i * gamma * H_C) where H_C is the cost Hamiltonian

        Args:
            gamma: gamma (scalar) parameter in QAOA

        Returns: e^(-i * gamma * H_c) as a quantum circuit
        """
        circuit = qi.QuantumCircuit(self.num_qubits, self.num_qubits)
        for (u, v) in self.wgraph.edges:
            circuit.cx(u, v)
            circuit.rx(2.0 * gamma, v)
            circuit.cx(u, v)
        return circuit

    def mixer_operator(self, beta):
        """
        Description: defines the mixer operator e^(-i * beta * H_M) where H_M is the mixer Hamiltonian

        Args:
            beta: beta (scalar) parameter in QAOA

        Returns: e^(-i * beta * H_c) as a quantum circuit
        """
        circuit = qi.QuantumCircuit(self.num_qubits, self.num_qubits)
        for q in range(self.num_qubits):
            circuit.rx(2.0 * beta, q)
        return circuit

    def build_circuit(self, params):
        """
        Description: defines the complete QAOA circuit

        Args:
            params: (gamma, beta) complete parameter set for QAOA

        Returns: the complete QAOA circuit
        """
        circuit = qi.QuantumCircuit(self.num_qubits, self.num_qubits)
        depth = int(len(params) / 2)
        # initialize the qubits with the Hadamard gate
        circuit.h(range(self.num_qubits))
        # add cost and mixer operators
        for i, gamma in enumerate(params[:depth]):
            circuit += self.cost_operator(gamma)
            circuit += self.mixer_operator(params[depth + i])
        # measure the qubits
        circuit.barrier(range(self.num_qubits))
        circuit.measure(range(self.num_qubits), range(self.num_qubits))
        return circuit

    def run_circuit(self, circuit, num_shots):
        """
        Description: performs multi-shot execution of QAOA circuit

        Args:
            circuit: QAOA circuit to execute
            num_shots: number of simulations

        Returns: results of the simulation as a dictionary with bit-strings as keys
        """
        simulation = qi.execute(circuit, self.simulator, shots=num_shots)
        result = simulation.result().get_counts()
        # take care of little endianness of Qiskit and return the result
        return {bit_string[::-1]:value for bit_string, value in result.items()}

    def build_objective(self, num_shots):
        """
        Description: defines the final max-cut objective

        Args:
            num_shots: number of simulations per run of the objective function

        Returns: the complete max-cut objective as a real-valued function of params = (gamma, beta)
        """
        def func(params):
            cost = 0.0
            circuit = self.build_circuit(params)
            result = self.run_circuit(circuit, num_shots)
            for bit_string, value in result.items():
                cost += value * self.classical_objective(bit_string)
            return cost / num_shots
        self.objective = func

    def solve(self, depth, max_iter):
        """
        Description: solves the max-cut problem with QAOA and stores
                     the sorted array of cuts (as bit_strings) in the decreasing order of probability of being optimal

        Args:
            depth: depth of QAOA
            max_iter: maximum number of iterations for scipy optimizer
        """
        # solve for QAOA parameters
        initial_guess = np.ones(2 * depth)
        optimization_result = minimize(self.objective, initial_guess, method='COBYLA', options={'maxiter': max_iter})
        # map the optimal QAOA paramters to the bit-string(s) representing the solution(s) of max-cut
        optimal_params = optimization_result['x']
        circuit = self.build_circuit(optimal_params)
        simulation_result = self.run_circuit(circuit, 1000)
        # plot histogram of simulation results
        bit_strings = list(simulation_result.keys())
        probabilities = [simulation_result[bs] / 1000.0 for bs in bit_strings]
        plt.bar([int(bs, 2) for bs in bit_strings], probabilities)
        plt.title('probabilities of being an optimal cut')
        plt.show()
        # sort cuts according to probabilities in a decreasing order
        self.sols =  np.array(bit_strings)[np.argsort(probabilities)][::-1]
        
    def view_first_few_solutions(self, num_sols_to_display):
        """
        Description: displays first few solutions obtained by QAOA
        
        Args:
            num_sols_to_display: number of solutions to be displayed
        """
        print("Here are the first {} candidates for optimal cut with corresponding sums of inter-cluster edge weights:".format(num_sols_to_display)) 
        for i, sol in enumerate(self.sols[:num_sols_to_display]):
            string = "Candidate #{} for optimal cut".format(i)
            print("{}\n{}".format(string, '-' * len(string)))
            print("Cut{}: Sum of inter-cluster edge weights".format(' ' * (self.num_qubits - 3) if self.num_qubits > 2 else 0))
            print("{}: {}".format(sol, abs(0.5* self.classical_objective(sol))))
            self.wgraph.draw(cut=sol)