from tkinter import Tk
from tkinter.filedialog import askopenfilename
from assembly_line import AssemblyLine
from simulated_annealing_for_alb import SimulatedAnnealingForALB

Tk().withdraw()
filename = askopenfilename()
file = open(filename)
assembly_line = AssemblyLine(file, 6)

print(assembly_line.get_dependency_graph())
simulated_annealing_for_alb = SimulatedAnnealingForALB(assembly_line)

for workstation in simulated_annealing_for_alb.get_current_solution():
    print(workstation.tasks)


initial_temperature = 100
maximum_number_of_disturbances = assembly_line.get_number_of_workstations() * assembly_line.get_number_of_tasks()
cooling_rate = 0.01

print(str(simulated_annealing_for_alb.get_cycle_time_current_solution()) + '\n')

simulated_annealing_for_alb.run(initial_temperature, maximum_number_of_disturbances, cooling_rate)

print('\n')

for workstation in simulated_annealing_for_alb.get_current_solution():
    print(workstation.tasks)

print(simulated_annealing_for_alb.get_cycle_time_current_solution())
