class WorkStation:
    def __init__(self, workstation_identification, assembly_line):
        self.workstation_identification = workstation_identification
        self.tasks = []
        self.cycle_time = 0
        self.number_of_tasks = 0
        self.workstations_it_depends_on = set()
        self.idetification_of_workstations_it_depends_on = set()
        self.tasks_dependencies = set()
        self.__assembly_line = assembly_line

    def calculate_cycle_time(self):
        cycle_time = 0
        for task in self.tasks:
            cycle_time += self.__assembly_line.get_task_time(task)
        self.cycle_time = cycle_time
