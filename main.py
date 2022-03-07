def machineEpsilon(func=float):
    machine_epsilon = func(1)
    while func(1) + func(machine_epsilon) != func(1):
        machine_epsilon_last = machine_epsilon
        machine_epsilon = func(machine_epsilon) / func(2)
    return machine_epsilon_last

print(machineEpsilon())