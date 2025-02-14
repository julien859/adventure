import json

from location import Location
from item import Item


class Game:
    def __init__(
        self, 
        name, 
        location=None, 
        target=None,
        locations=None, 
        items=None
    ):
        self.name = name
        self.locations = {location['name']: Location(**location) for location in (locations or [])}
        self.items = {item["name"]: Item(**item) for item in (items or [])}
        self.done = False

        try:
            self.location = self.locations[location] if location else self.locations[locations[0]["name"]]
        except TypeError:
            self.location = None

        try:
            self.target = self.locations[target] if location else self.locations[locations[-1]["name"]]
        except TypeError:
            self.target = None

    def __str__(self):
        return self.name

    @classmethod
    def load(cls, filename):
        print('Loading game "%s"' % filename)
        with open(filename) as fin:
            data = json.load(fin)
        return Game(**data)

    def move(self, destination):
        if (destination in self.locations) and (destination in self.location.doors):
            self.location = self.locations[destination]
        else:
            raise KeyError("%s is vanuit %s niet te bereiken" % (destination, self.location))

    def get(self, item):
        if item in self.location.items:
            self.items.append(self.location.items[item])
            del self.location.items[item]
        else:
            raise KeyError("Er is geen %s in %s" % (item, self.location))

    def drop(self, item):
        if item in self.items:
            self.location.items.append(self.items[item])
            del self.items[item]
        else:
            raise KeyError("Er is geen %s in %s" % (item, self.location))

    def describe(self, key):
        description = ""
        if key in self.locations:
            location = self.locations[key]
            description = location.description
            if len(location.items) > 0:
                items = [str(item) for item in location.items]
                description += '\nEr liggen hier: %s' % ', '.join(items)
        elif key in self.location.items:
            description = self.location.items[key].description
        elif key in self.items:
            description = self.items[key].description
        elif key == 'spullen':
            items = [str(item) for item in self.items]
            description = ', '.join(items)

        return description