import qiskit as qi
import numpy as np
import math
from matplotlib import pyplot as plt
import random
from scipy.optimize import minimize 

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

    def classical_objective(self, bit_string):
        pass

    def cost_operator_unit(self, gamma):
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

    def mixer_operator_unit(self, beta):
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
            circuit += self.cost_operator_unit(gamma)
            circuit += self.mixer_operator_unit(params[depth + i])
        # measure the qubits
        circuit.barrier(range(self.num_qubits))
        circuit.measure(range(self.num_qubits), range(self.num_qubits))
        return circuit

    def build_objective(self, depth):
        """
        Description: defines the final max-cut objective

        Args:
            depth: depth of QAOA

        Returns: the complete max-cut objective as a real-valued function of params = (gamma, beta)
        """
        def func(params):
            circuit = self.build_circuit(params)
        pass