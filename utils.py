
class Set:

    def __init__(self):
        self.set = set([])

    def add(self, element):
        self.set.add(element)

    def size(self):
        return len(self.set)

    def contains(self, element):
        return self.set.issuperset({element})