import argparse
from basics.parser import Parser

parser = argparse.ArgumentParser(description='idk')
parser.add_argument('file', type=str, default='main.cld',help='file to read')

args = parser.parse_args()
parser = Parser()

def main():
    try:
        file = open(args.file, "r", encoding="utf-8").readlines()
    except Exception as e:
        print(e)
        exit(-1)

    for line in file:
        parser.parse_line(
            line.strip("\n")
        )
        
        
if __name__ == "__main__":
    main()
