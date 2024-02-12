class DependencyManager:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, name: str, dependency):
        self.dependencies[name] = dependency

    def get_dependency(self, name: str):
        return self.dependencies[name]

    def get_dependencies(self):
        return self.dependencies
