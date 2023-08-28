# Quantum-Search-Hamiltonian-simulation

This is a simulation of a certain type of quantum search Hamiltonian. The evolution under this Hamiltonian drives the system to a state corresponding to a solution to the search problem.
The program "improvedgeneralsearchhamiltonian" is a program in which the user decides the number of qubits describing our search space and the number of Trotter steps.
The solution to the search problem is [number of qubits]*'1' (all qubits in state 1). 
The program "test.py" is esseantially the same program but you may divide the execution of the program to 4 or some other number of CPU cores. This is not not a significant speed-up, as many 
libraries in python already use multiple cores at the same time (numpy, for example) so this might create some mix-ups during the process, although it does not obstruct the exeuction of the program.
The speed-up is around 1.2-1.5 times. 
