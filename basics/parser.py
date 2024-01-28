from typing import Any
from basics.namespace import NameSpace
import re


class Parser:
    def __init__(self):
        self.state = ""
        self.namespace = NameSpace()
        self.patterns = [
            (r'^\s*([^\d_]\w*)\s*\(\s*([\s\S]*?)\s*\)\s*$',  self.execute_function, 'executable'),
            (r'^\s*(\w+)\s=\s*(.+?)\s*$', self.create_const, 'const'),
            (r'^\s*(\w+)\s[+](\w+)*$', self.mathematic, 'math')
        ]
    
    def parse_line(self, line) -> Any:
        for pattern in self.patterns:
            res = re.match(pattern[0], line)
            if res and pattern[2] == 'executable':
                name = res.group(1)
                args = res.group(2)
                if re.match(pattern[0], args):
                    args = self.parse_line(args)
                    
                return pattern[1](name, args)

            elif res and pattern[2] == "math":
                a = res.group(1)
                b = res.group(2)

                pattern[1](a, b)

            elif res and pattern[2] == "const":
                name = res.group(1)
                value = res.group(2)
                if re.match(self.patterns[0][0], value):
                    value = self.parse_line(value)
                
                pattern[1](name, value)
            
            else:
                print("Unknown logic:")
                print(f"{line}")
                exit(-1)
            
    
    def mathematic(self, y, x):
        if x.isdigit() and y.isdigit():
            pass 
        else:
            print(f"TypeError: a or b not a number")
            
        return int(x) + int(y)
            
    def create_const(self, name, value):
        if value.isdigit():
            pass
        
        elif not value.startswith('"') and not value.endswith('"'):
            try:
                value = self.namespace.check_namespace(value, "const")
            except NameError:
                print(f'NameError: {value} does not exist (line UNKNOWN)')
                exit(-1) 

        elif value.startswith('"') and not value.endswith('"') or not value.startswith('"') and value.endswith('"'):
            print(f'SyntaxError: excepted " on line: {value}')
            exit(-1) 

        elif value.startswith('"') and value.endswith('"'):
            value = value.strip('"')
        
        self.namespace.update_namespace(name, value)
        
    def update_const(self, name, value):
        if value.isdigit():
            name = self.namespace.check_namespace(name, "const")
            name = name + value
        else:
            print(f"TypeError: cannot add {value} to {name}")
            exit(-1)
        self.namespace.update_namespace(name, value)
            
    def execute_function(self, name, args: str):
        res = self.namespace.check_namespace(name, 'function')
        
        if args is None:
            args = "Nothing"
            
        elif not args:
            print(f"RequiredError: required args is nothing!", end="")
            
        elif args.isdigit():
            pass
        
        elif not args.startswith('"') and not args.endswith('"'):
            try:
                args = self.namespace.check_namespace(args, "const")
            except NameError:
                print(f'NameError: {args} does not exist (line UNKNOWN)')
                exit(-1) 

        elif args.startswith('"') and not args.endswith('"') or not args.startswith('"') and args.endswith('"'):
            print(f'SyntaxError: excepted " on line: {args}')
            exit(-1) 

        elif args.startswith('"') and args.endswith('"'):
            args = args.strip('"')
        
        return res(args)
        

