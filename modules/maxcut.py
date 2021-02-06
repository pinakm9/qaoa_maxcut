import cirq
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
        self.qubits = [cirq.GridQubit(0, i) for i in range(self.wgraph.number_of_node())]

    def qubit_init(self):
        """
        Description: even superposition initializer for qubits

        Yields: the initialized qubits
        """
        for qb in self.qubits:
            yield cirq.H.on(qb)

    def cost_unitary(self, gamma):
        """
        Description: defines the cost Hamiltonian

        Args:
            gamma: gamma parameter in QAOA

        Yields: tensor product of two Z gates raised by an exponent -gamma/pi
        """
        for (u, v) in self.wgraph.edges:
            yield cirq.ZZPowGate(exponent=-gamma/math.pi).on(qubits[u], qubits[v])

    def mixer_unitary(self, alpha):
        """
        Description: defines the mixer Hamiltonian

        Args:
            alpha: alpha parameter in QAOA

        Yields: X gates raised by an exponent -alpha/pi
        """
        for qb in self.qubits:
            yield cirq.XPowGate(exponent=-alpha/math.pi).on(qb)

    def create_circuit(self, depth, params, rep):

        gamma = [params[0], params[2], params[4], params[6]]
        alpha = [params[1], params[3], params[5], params[7]]

        self.circuit = cirq.Circuit()
        self.circuit.append(self.qubit_init())
        for i in range(depth):
            self.circuit.append(self.cost_unitary(gamma[i]))
            self.circuit.append(self.mixer_unitary(alpha[i]))
        self.circuit.append(cirq.measure(*qubits, key='x'))
        print(self.circuit)

        simulator = cirq.Simulator()
        results = simulator.run(self.circuit, repetitions=rep)
        results = str(results)[2:].split(", ")
        new_res = []
        for i in range(rep):
            hold = []
            for j in range(len(self.qubits)):
                hold.append(int(results[j][i]))
            new_res.append(hold)

        return new_res