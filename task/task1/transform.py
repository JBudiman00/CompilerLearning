import json
import sys

def countMathOperations():
    prog = json.load(sys.stdin)
    operationCount = {
        'add': 0,
        'sub': 0,
        'mul': 0,
        'div': 0
    }
    for func in prog['functions']:
        for line in func['instrs']:
            if line['op'] in operationCount:
                operationCount[line['op']] += 1
    print(operationCount)

if __name__ == '__main__':
    countMathOperations()
