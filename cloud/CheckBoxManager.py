__author__ = 'gumengyuan'

class CheckBoxManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.boxes = {}

    def add(self, name, value):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "%s" % name

        self.boxes[tag] = value
        return "check", tag

    def click(self, name):
        tag = "%s" % name
        self.boxes[tag] = 1 - self.boxes[tag]

    def get(self):
        checked = []
        for tag in self.boxes.keys():
            if self.boxes[tag] == 1:
                self.links[tag]()
                checked.append(tag)
        return checked