#Import all needed tools

#For using all cores simultaneously
from multiprocessing import Pool

num_cores = 4

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np
from qiskit.compiler import transpile
from qiskit.tools.visualization import plot_histogram
from qiskit.circuit.library import MCXGate

import matplotlib.pyplot as plt

import datetime

#How many qubits do you want in your search space? 
k = 5

correct_index = '1'*k

#How many simulation steps in your simulation? 
n = 7

#Define a function of a single variable: the number of simulations. 
def simulator(num_aer: int):
    
    print('Start time: ', datetime.datetime.now())
    #Create quantum registers for search space and the oracle

    #Search space
    register = QuantumRegister(k, name="q")

    #Oracle workspace
    ancilla = QuantumRegister(1, name="ancilla") 

    #Classical register to save information from qubits during measurement
    classical = ClassicalRegister(k, 'Classical bits')


    # Create a Quantum Circuit acting on the quantum register and add the ancilla

    circuit = QuantumCircuit(register, ancilla, classical)


    #We need to create a uniform superposition, because qiskit prepares everything in state 0 and for some reason nothing works without this
    for i in range(k): 
        circuit.h(i)
        
        
    #Multicontrol qubit
    gate = MCXGate(k)

    t = np.sqrt(2**k)*np.pi/2
    a = 1
    dt = t / n

    #Create a list of qubit indices: 
    qubits = []
    for i in range(k): 
        qubits.append(i)

    qubits.append(ancilla)

    print(qubits)
    for i in range(n): 
        
        #Oracle is the multicontrolled CNOT because the correct answer is 11111.
        circuit.append(gate, qubits)

        #Phase gate
        circuit.p(-a*dt, ancilla)

        #Oracle
        circuit.append(gate, qubits)

        
        #Driving hamiltoninan |psi><psi|
        
        #Walsh-Hadamard
        for i in range(k): 
            circuit.h(i)
        
        #Pauli X gates
        for i in range(k): 
            circuit.x(i)

        #Control gate
        circuit.append(gate, qubits)
        
        #Pauli X gates
        for i in range(k): 
            circuit.x(i)

        #Phase gate
        circuit.p(-a*dt, ancilla)

        #Pauli X gates
        for i in range(k):
            circuit.x(i)

        #Control gate
        circuit.append(gate, qubits)
        
        #Pauli X gates
        for i in range(k): 
            circuit.x(i)
            
        #Walsh-Hadamard
        for i in range(k): 
            circuit.h(i)
        
        circuit.barrier()

    circuit.measure(register, classical)

    qasm_simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(circuit, qasm_simulator)
    result = qasm_simulator.run(transpiled_qc, shots=num_aer, memory=False).result()

    correct = result.get_counts()[correct_index]

    data = {correct_index: correct, 'Other': num_aer - correct}
    
    return data

if __name__ == "__main__":
    #Define arguments that we wish to give the simulator-function. Aer will run each simulation 256 times and multiprocessing will run it on 4 cores (=1024 total). 
    list_of_args = [256, 256, 256, 256]
        
        #Create a pool of worker class processes to execute the function in parallel
    with Pool(processes=num_cores) as pool:
        results = pool.map(simulator, list_of_args)
            
        #Count the total number of solutions
    num_correct_state = 0

        #Count the total number of non-solutions
    num_others = 0

        #Count all the results together
    for item in results: 
        num_correct_state += item[correct_index]
        num_others += item['Other']

    #Add results to dictionary for histograms
    total_data = {correct_index: num_correct_state, 'Other': num_others}
    print('Program finished at: ', datetime.datetime.now())
    #Draw histograms
    plot_histogram(total_data, title= f"{n} simulaatioaskelta")
    plt.show()
    
    