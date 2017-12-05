from __future__ import print_function

import time
import os
import os.path as op
import deepmind_lab_gym as dlg
import cv2
import numpy as np
import sys
sys.path.insert(0, op.join(op.dirname(__file__) or '.', '../openai-a3c-impl'))
from multiprocgym import MultiProcGym

def demo_random_mazes(level_script="tests/demo_map"
                      , multiproc=True, multiproc_use_threads=False):
    env = dlg.register_and_make(level_script
                                , dict(width=84, height=84, fps=30)
                                , dlg.ActionMapper("discrete")
                                , additional_observation_types=[])
    if multiproc:
        env = MultiProcGym(env, 3, use_threads=multiproc_use_threads)

    start_time = time.time()
    for i in range(600*30):
        obs, reward, terminal, info = env.step(env.action_space.sample())
        print("\r{}".format(i),end='')
        if terminal:
            print("env.reset() time_take = {}".format(time.time() - start_time))
            start_time = time.time()
            env.reset()

if __name__ == '__main__':
    start_time = time.time()
    demo_random_mazes(multiproc=True, multiproc_use_threads=True)
    print("multiproc use processes {}".format(time.time() - start_time))
    start_time= time.time()
    demo_random_mazes(multiproc=True, multiproc_use_threads=False)
    print("multiproc use threads {}".format(time.time() - start_time))
    start_time= time.time()
    demo_random_mazes(multiproc=False)
    print("No multiproc {}".format(time.time() - start_time))
    
