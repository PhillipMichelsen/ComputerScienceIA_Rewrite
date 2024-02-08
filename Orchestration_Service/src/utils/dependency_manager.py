class DependencyManager:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, name, dependency):
        self.dependencies[name] = dependency

    def get_dependency(self, name):
        return self.dependencies[name]

    def get_dependencies(self):
        return self.dependencies
