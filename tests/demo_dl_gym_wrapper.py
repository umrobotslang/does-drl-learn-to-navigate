import os
import sys
import os.path as op
import glob

import deepmind_lab_gym as dlg
import multiprocdmlab as mpdmlab
import cv2
import numpy as np
from top_view_renderer import MatplotlibVisualizer

discretekey2action = {  'd' : 0
                        , 'a' : 1
                        , 'w' : 2
                        , 's' : 3 }
acceleration_key2action = {  'd' : 2
                           , 'a' : 3
                           , 'w' : 4
                           , 's' : 5
                           , 'o' : 0
                           , 'p' : 1
                           , 'z' : 6
                           , 'c' : 7 }

def run_env_interactively2(env
                           , key2action = discretekey2action):
    key = 'a'
    imgdir = '/tmp/dhiman_dl/'
    if not op.exists(imgdir) : os.makedirs(imgdir)
    i = 0
    # Play 5 episodes
    for n in range(3):
        print(" Playing episode %d " % n)
        terminal = False
        while not terminal:
            obs, reward, terminal, info = env.step(key2action[key])
            print("INFO['GOAL.LOC'] : {}".format(info.get('GOAL.LOC')))
            print("INFO['SPAWN.LOC'] : {}".format(info.get('SPAWN.LOC')))
            if terminal: print("Got terminal")
            #im, fig = env.render(mode='return')
            #mplibvis.print_figure(fig, op.join(imgdir, 'top_view_%05d.png' % i), dpi=84)
            cv2.imshow("c", obs)
            k = cv2.waitKey(-1)
            if k != -1:
                if chr(k & 255) == 'q':
                    break
                elif chr(k & 255) in key2action:
                    key = chr(k & 255)
            i = i+1
        env.reset()

def run_env_interactively(env):
    key2action = {  'd' : 0
                  , 'a' : 1
                  , 'w' : 2
                  , 's' : 3}
    mplibvis = MatplotlibVisualizer()

    key = 'a'
    obs, fig = env.reset()
    cv2.imshow("c", obs)
    k = cv2.waitKey(33)
    if k != -1 and chr(k & 255) in key2action:
        key = chr(k & 255)

    terminal = False
    while not terminal:
        obs, reward, terminal, info = env.step(key2action[key])
        im, fig = env.render(mode='return')
        cv2.imshow("c", im)
        #mplibvis.render(fig)
        k = cv2.waitKey(33)
        if k != -1 and chr(k & 255) in key2action:
            key = chr(k & 255)
        elif k != -1 and chr(k & 255) == 'q':
            break
    

def demo_small_star_map_continuous_spawn():
    print("Loading deepmind_lab_gym from %s" % dlg.__file__)
    level_script = "small_star_map_continuous_spawn_01"
    env = dlg.register_and_make(level_script
                          , dict(width=320, height=320, fps=30
                                , noclip="true")
                          , dlg.ActionMapper("discrete")
                               , additional_observation_types=["GOAL.LOC",
                                                               "POSE", "GOAL.FOUND"])
    run_env_interactively(env)


def demo_small_map_test_mode(level_script):
    print("Loading deepmind_lab_gym from %s" % dlg.__file__)
    env = dlg.register_and_make(level_script
                                , dict(width=320, height=320, fps=30)
                                , dlg.ActionMapper("discrete")
                                , additional_observation_types=[
                                    "GOAL.LOC", "POSE", "GOAL.FOUND"])
    run_env_interactively(env)

def demo_small_map_wall_penalty(level_script):
    print("Loading deepmind_lab_gym from %s" % dlg.__file__)
    env = dlg.register_and_make(level_script
                                , dict(width=320, height=320, fps=30)
                                , dlg.ActionMapper("discrete")
                                , wall_penalty_max_dist = 30
                                , wall_penalty_max = 0.2)
    run_env_interactively(env)

def demo_discrete_big_steps(level_script):
    print("Loading deepmind_lab_gym from %s" % dlg.__file__)
    env = dlg.register_and_make(level_script
                                , dict(width=320, height=320, fps=30)
                                , dlg.ManhattanWorldActionMapper_v0
                                , additional_observation_types = ['POSE']
                                , init_game_seed = 0)
    run_env_interactively2(env)

def demo_random_mazes(level_script='random_mazes'
                      , rows=9
                      , cols=9
                      , mode='training'
                      , num_maps = 100):
    env = dlg.register_and_make(level_script
                                , dict(width=320, height=320, fps=30
                                       , rows = rows
                                       , cols = cols
                                       , mode = mode
                                       , num_maps = num_maps
                                       , random_spawn_random_goal = "True"
                                       , apple_prob = 0.1
                                       , episode_length_seconds = 20)
                                , dlg.ActionMapper("discrete")
                                , additional_observation_types=[
                                    "GOAL.LOC", "POSE", "GOAL.FOUND"]
                                , entry_point_object=mpdmlab.RandomMazesDMLab)

    run_env_interactively2(env)

def demo_random_mazes_mp(level_script = 'random_mazes'
                         , rows = 9
                         , cols = 9
                         , mode ='training'
                         , num_maps = 1000):
    env = mpdmlab.MultiProcDeepmindLab(
        dlg.DeepmindLab
        , level_script
        , dict(width=320, height=320, fps=30
               , rows = rows
               , cols = cols
               , mode = mode
               , num_maps = 1
               , withvariations = True
               , random_spawn_random_goal = "True"
               , chosen_map = "training-09x09-0127"
               , mapnames = "training-09x09-0127"
               #, mapnames = "seekavoid_arena_01"
               , mapstrings =
               open("deepmind-lab/assets/entityLayers/09x09/training/entityLayers/0127.entityLayer").read()
               , apple_prob = 0.9
               , episode_length_seconds = 5)
        #, dlg.L2NActionMapper_v0
        , dlg.ActionMapperDiscrete
        , additional_observation_types=[
            "GOAL.LOC", "SPAWN.LOC", "POSE", "GOAL.FOUND"]
        , mpdmlab_workers = 1
    )
    run_env_interactively2(env, discretekey2action)
    
if __name__ == '__main__':
    import sys
    kwargs = {}
    if len(sys.argv[1:]):
        kwargs["level_script"] = sys.argv[1]
    #demo_small_star_map_continuous_spawn()
    #demo_small_map_test_mode(level_script)
    #level_script = "small_star_map_continuous_spawn_25"
    #demo_small_map_test_mode(level_script)
    #demo_small_map_wall_penalty(level_script)
    #level_script = 'seekavoid_arena_01'
    #demo_map_simplest(level_script)
    #demo_discrete_big_steps("small_star_map_random_goal_01")
    demo_random_mazes_mp(**kwargs)
