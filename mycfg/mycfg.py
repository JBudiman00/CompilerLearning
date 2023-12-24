import json
import sys
from collections import OrderedDict

TERMINATORS = 'jmp', 'br', 'ret'

def form_blocks(body):
    cur_block = []

    for instr in body:
        if 'op' in instr:
            cur_block.append(instr)

            if instr['op'] in TERMINATORS:
                yield cur_block
                cur_block = []
        else:
            yield cur_block
            cur_block = [instr]

    yield cur_block
            
def block_map(blocks):
    out = OrderedDict()
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))

        out[name] = block

    return out

def get_cfg(name2block):
    cfg = {}
    i = 0
    for name, block in name2block.items():
        last = block[-1]
        if last['op'] in  ('jmp', 'br'):
            succ = last['labels']
        elif last['op'] == 'ret':
            succ = []
        else:
            if i == len(name2block) - 1:
                succ = []
            else:
                succ = [list(name2block.keys())[i+1]]
        i += 1
        cfg[name] = succ
    return cfg
            

def mycfg():
    prog = json.load(sys.stdin)
    blocks = []
    for func in prog['functions']:
        for block in form_blocks(func['instrs']):
            blocks.append(block)
    name2block = block_map(blocks)
    cfg = get_cfg(name2block)
    print(cfg)


if __name__ == '__main__':
    mycfg()
