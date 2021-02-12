import cirq
# Pick a qubit.
qubit1 = cirq.GridQubit(0, 0)
qubit2 = cirq.GridQubit(0, 1)
# Create a circuit
circuit = cirq.Circuit(
    #cirq.X(qubit)**0.5,  # Square root of NOT.
    cirq.ZZPowGate(exponent=-0.5).on(qubit1, qubit2),  # Square root of NOT.
    #cirq.measure(qubit, key='m')  # Measurement.
)
print("Circuit:")
print(circuit)

# Simulate the circuit several times.
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)
