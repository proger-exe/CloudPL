

class NameSpace:
    def __init__(self):
        self.namespace = {
            "echo": ('function', print),
            "ver": ('const', '0.1b'),
            "write": ('function', input)
        }
        
    def check_namespace(self, name: str, namespace_type):
        if name not in self.namespace:
            raise NameError(f'{name} does not exist')
        elif self.namespace[name][0] != namespace_type:
            raise TypeError(f"{name} cannot be executable")
        
        return self.namespace[name][1]
    
    def update_namespace(self, name: str, value: str):
        self.namespace.update({name: ('const', value)})            
