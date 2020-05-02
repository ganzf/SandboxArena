import time
import sys

class DoubleBuffer(object):
    def __init__(self):
        self.main_buffer = []
        self.second_buffer = {}
        self.remove_buffer = {}
        self.requires_add = False
        self.requires_remove = False

    def get_list(self):
        return self.main_buffer

    def add(self, value):
        self.requires_add = True
        self.second_buffer[value.id] = value
    
    def remove(self, value):
        # We would mark an item for removal but it would not be added yet
        if value.id in self.second_buffer.keys():
            return
        self.requires_remove = True
        self.remove_buffer[value.id] = value

    def update(self):
        if self.requires_add or self.requires_remove:
            next = []
            if self.requires_add:
                if self.requires_remove:
                    for item in self.main_buffer:
                        if item.id not in self.remove_buffer.keys():
                            next.append(item)
                        else:
                            item.remove()
                    # list contains kept items from main buffer + new items
                    next += list(self.second_buffer.values())
                else:
                    next = list(self.second_buffer.values()) + self.main_buffer
            elif self.requires_remove:
                for item in self.main_buffer:
                    if item.id not in self.remove_buffer.keys():
                        next.append(item)
                    else:
                        item.remove()
                            
            self.main_buffer = next
            self.requires_add = False
            self.requires_remove = False
            self.second_buffer = {}
            self.remove_buffer = {}

class Store(object):
    def __init__(self):
        self.values = {}
        self.entity_index = {}
        self.total_time = 0.0
        self.times = {}
        self.timers_allowed = True
        self.debug = False

        # Fast access to most important components
        self.transforms = DoubleBuffer()
        self.visibles = DoubleBuffer()
        self.chunkless = DoubleBuffer()
        self.chunks = DoubleBuffer()

    def disable_timers(self):
        self.timers_allowed = False

    def add(self, name, value):
        self.values[name] = value

    def add_to(self, path, value):
        if path == 'entities':
            self.entity_index[value.id] = value
        self.values[path].append(value)

    def get(self, name):
        return self.values.get(name)

    def components(self, componentName):
        entities = self.get("entities")
        list = []
        if entities:
            for entity in entities:
                c = entity.components.get(componentName)
                if c:
                    list.append(c)
        return list

    def entity(self, componentOrId, fast=False):
        if fast:
            return self.entity_index.get(id)
        entities = self.get('entities')
        if entities:
            for entity in entities:
                if entity.id == id:
                    return entity
        return None

    def begin_time(self, name):
        if not self.timers_allowed:
            return 
        if not self.times:
            self.times = {
                'last': {},
                'sum': {},
                'avg': {},
                'counts': {},
            }
        if not self.times['sum'].get(name):
            self.times['sum'][name] = 0.0
            self.times['counts'][name] = 0.0
            self.times['avg'][name] = 0.0
        self.times['last'][name] = time.time()
        
    def end_time(self, name):
        if not self.timers_allowed:
            return 
        last = time.time() - self.times['last'][name]
        self.times['last'][name] = last
        self.times['sum'][name] += last
        self.times['counts'][name] += 1
        self.times['avg'][name] = self.times['sum'][name] / self.times['counts'][name]


store = Store()