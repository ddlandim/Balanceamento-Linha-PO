from simulated_annealing import SimulatedAnnealing
from workstation import WorkStation
import math
import random


class SimulatedAnnealingForALB(SimulatedAnnealing):
    INFINITE_CYCLE_TIME = 100000
    MIN_TEMPERATURE = 0.001

    def __init__(self, assembly_line):
        self.__assembly_line = assembly_line
        self.__current_solution = self.__build_initial_solution()
        self.__cycle_time_current_solution = self.__calculate_cycle_time(self.__current_solution)


    def run(self, initial_temperature, maximum_number_of_disturbances, cooling_rate):
        self.__current_solution = self.__build_initial_solution()
        temperature = initial_temperature * 1.0
        cont = 0
        while temperature >= self.MIN_TEMPERATURE:
            cont += 1
            number_of_distubances = 0
            while number_of_distubances < maximum_number_of_disturbances:
                number_of_distubances += 1
                new_solution = self.__disturb_current_solution(self.__current_solution)
                cycle_time = self.__calculate_cycle_time(new_solution)
                delta_e = cycle_time - self.__cycle_time_current_solution
                if delta_e <= 0:
                    self.__current_solution = new_solution
                    self.__cycle_time_current_solution = cycle_time
                elif random.uniform(0, 1) <= self.__calculate_probability(delta_e, temperature):
                    self.__current_solution = new_solution
                    self.__cycle_time_current_solution = cycle_time
            temperature = temperature * (1 - cooling_rate)
            print(temperature)

    def __disturb_current_solution(self, solution):
        new_solution = solution.copy()
        workstation1 = new_solution[random.randint(0, len(new_solution) - 1)]
        workstation2 = new_solution[random.randint(0, len(new_solution) - 1)]

        task1 = workstation1.tasks[random.randint(0, len(workstation1.tasks) - 1)]
        task2 = workstation2.tasks[random.randint(0, len(workstation2.tasks) - 1)]

        workstation1.tasks.remove(task1)
        workstation1.tasks.append(task2)

        workstation2.tasks.remove(task2)
        workstation2.tasks.append(task1)

        return solution

    def __calculate_probability(self, delta_e, temperature):
        return math.exp(-delta_e/float(temperature))


    def __build_initial_solution(self):
        unallocated_tasks = self.get_tasks_ordered_by_number_of_dependencies()
        workstations = []
        approximate_number_of_tasks_per_workstation = self.__assembly_line.get_number_of_tasks() / self.__assembly_line.get_number_of_workstations()
        workstation_identification = 1
        workstation = WorkStation(workstation_identification, self.__assembly_line)
        number_of_tasks_in_this_workstation = 0

        while len(unallocated_tasks) > 0:
            if number_of_tasks_in_this_workstation >= approximate_number_of_tasks_per_workstation and \
                    len(workstations) < self.__assembly_line.get_number_of_workstations():
                workstations.append(workstation)
                number_of_tasks_in_this_workstation = 0
                workstation_identification += 1
                workstation = WorkStation(workstation_identification, self.__assembly_line)

            rand_index = -1#random.randint(0, len(unallocated_tasks) - 1)
            rand_task = unallocated_tasks[rand_index]
            unallocated_tasks.remove(rand_task)

            workstation.tasks.append(rand_task)
            number_of_tasks_in_this_workstation += 1

        workstations.append(workstation)

        return workstations

    def get_tasks_ordered_by_number_of_dependencies(self):
        ordered_tasks = list(self.__assembly_line.get_list_of_tasks())
        for i in range(len(ordered_tasks)):
            for j in range(len(ordered_tasks)):
                number_of_dependencies_i = len(self.__assembly_line.get_dependency_graph()[ordered_tasks[i]])
                number_of_dependencies_j = len(self.__assembly_line.get_dependency_graph()[ordered_tasks[j]])
                if number_of_dependencies_i > number_of_dependencies_j:
                    aux = ordered_tasks[i]
                    ordered_tasks[i] = ordered_tasks[j]
                    ordered_tasks[j] = aux
        return ordered_tasks


    def __get_workstations_precedencies_and_dependencies(self, solution):
        workstations_a_workstation_preceeds = {}
        workstations_a_workstation_depends_on = {}
        for workstation in solution:
            tasks_the_workstation_depends_on = set()
            for task in workstation.tasks:
                task_dependencies = self.__assembly_line.get_dependency_graph()[task]
                for task_dependency in task_dependencies:
                    if task_dependency not in workstation.tasks:
                        tasks_the_workstation_depends_on.add(task_dependency)

            for other_workstation in solution:
                if workstation.workstation_identification == other_workstation.workstation_identification:
                    continue

                if len(tasks_the_workstation_depends_on.intersection(other_workstation.tasks)) > 0:
                    if other_workstation.workstation_identification not in workstations_a_workstation_preceeds.keys():
                        workstations_a_workstation_preceeds[other_workstation.workstation_identification] = set()
                    workstations_a_workstation_preceeds[other_workstation.workstation_identification].add(
                        workstation.workstation_identification)
                    if workstation.workstation_identification not in workstations_a_workstation_depends_on.keys():
                        workstations_a_workstation_depends_on[workstation.workstation_identification] = set()
                    workstations_a_workstation_depends_on[workstation.workstation_identification].add(
                        other_workstation.workstation_identification)

        return workstations_a_workstation_depends_on, workstations_a_workstation_preceeds

    def __is_solution_is_valid(self, solution):
        workstations_a_workstation_depends_on, workstations_a_workstation_preceeds = \
            self.__get_workstations_precedencies_and_dependencies(solution)

        for workstation in solution:
            if workstation.workstation_identification not in workstations_a_workstation_depends_on.keys() or \
                    workstation.workstation_identification not in workstations_a_workstation_preceeds.keys():
                continue
            if len(workstations_a_workstation_depends_on[workstation.workstation_identification]
                           .intersection(workstations_a_workstation_preceeds[workstation.workstation_identification])) > 0:
                return False
        return True

    def __calculate_cycle_time(self, solution):
        if not self.__is_solution_is_valid(solution):
            return self.INFINITE_CYCLE_TIME # penalizar soluções não factíveis

        max_cycle_time = 0
        for workstation in solution:
            workstation.calculate_cycle_time()
            if workstation.cycle_time > max_cycle_time:
                max_cycle_time = workstation.cycle_time

        return max_cycle_time

    def get_current_solution(self):
        return self.__current_solution

    def get_cycle_time_current_solution(self):
        return self.__cycle_time_current_solution
