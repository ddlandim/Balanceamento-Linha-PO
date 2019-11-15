class AssemblyLine():
    def __init__(self, file, number_of_workstations):
        self.__build_assembly_line(file, number_of_workstations)

    def __build_assembly_line(self, file, number_of_workstations):
        file_lines = []
        for line in file.readlines():
            if "-1" in line:
                break
            file_lines.append(line)
        self.__set_number_of_tasks(file_lines)
        self.__set_task_times(file_lines)
        self.__set_list_of_tasks(list(self.__task_time.keys()))
        self.__set_dependency_graph(file_lines)
        self.__build_map_of_tasks_a_task_can_preceed()
        self.__set_number_of_workstations(number_of_workstations)

    def __set_number_of_tasks(self, file_lines):
        self.__number_of_tasks = int(file_lines[0])

    '''
    Format of in2-files:
        line 1: number n of tasks
        lines 2-n+1: integer task times
        lines n+2,...: direct precedence relations in form "i,j"
        last line: end mark "-1,-1" (optional)
    '''
    def __set_task_times(self, file_lines):
        self.__task_time = {}
        for task in range(1, self.__number_of_tasks + 1):
            self.__task_time[task] = int(file_lines[task])

    def __set_list_of_tasks(self, list_of_tasks):
        self.__list_of_tasks = list_of_tasks

    def __set_number_of_workstations(self, number_of_workstations):
        self.__number_of_workstations = number_of_workstations

    def get_dependency_graph(self):
        return self.__dependency_graph;

    def get_number_of_tasks(self):
        return self.__number_of_tasks

    def get_task_time(self):
        return self.__task_time

    def get_task_time(self, task):
        return self.__task_time[task]

    def get_list_of_tasks(self):
        return self.__list_of_tasks

    def get_number_of_workstations(self):
        return self.__number_of_workstations

    # para cada tarefa, utilizando as relações de precedencia, lista as tarefas que precisam ser executadas antes dela, direta e indiretamente
    def __set_dependency_graph(self, file_lines):
        precedence_relations = []
        for relation in file_lines[self.__number_of_tasks + 1:]:
            precedence_relations.append(relation)

        self.__dependency_graph = {}
        for task in self.__list_of_tasks:
            self.__dependency_graph[task] = set()

        for relation in precedence_relations:
            relation_tuple = relation.split(',')
            task = int(relation_tuple[1])
            task_dependency = int(relation_tuple[0])
            self.__dependency_graph[task].add(task_dependency)

        already_calculated = {}
        for task in self.__dependency_graph.keys():
            self.__dependency_graph[task] = self.__get_all_dependencies_of_a_task(task, already_calculated)

    def __get_all_dependencies_of_a_task(self, task, already_calculated):
        if task in already_calculated.keys():
            return already_calculated[task]

        if len(self.__dependency_graph[task]) == 0:
            return set()

        dependencies = set()
        for task_dependency in self.__dependency_graph[task]:
            task_dependency_dependencies = self.__get_all_dependencies_of_a_task(task_dependency, already_calculated)
            already_calculated[task_dependency] = task_dependency_dependencies
            for dependency in task_dependency_dependencies:
                dependencies.add(dependency)
            dependencies.add(task_dependency)

        return dependencies

    def __build_map_of_tasks_a_task_can_preceed(self):
        self.__tasks_a_task_can_preceed = {}
        for task in self.__list_of_tasks:
            self.__tasks_a_task_can_preceed[task] = set()
            for preceded_task in self.__list_of_tasks:
                if task != preceded_task and preceded_task not in self.__dependency_graph[task]:
                    self.__tasks_a_task_can_preceed[task].add(preceded_task)






