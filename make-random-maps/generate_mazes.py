"""
Python program to generate and run a deepmind-lab based dqn 
experiment on the cluster. 
The code uses the jinja templating language to fill in 
certain fields of a pbs template script. 
Data is organized and stored via the amalgamation of the 
date of creation and the hyper-parameters of the network.
"""

from __future__ import print_function
import click
import jinja2
import os
import datetime
import subprocess
from shutil import copyfile
import numpy as np
import random
import math
import time
import sys

def getRandomEvenCoordinate(rows, cols):
    # Shape must be bigger than 2 and odd
    assert (rows > 2 and rows % 2 == 1)
    assert (cols > 2 and cols % 2 == 1)
    
    rowIdx = 2*int(random.randint(1, math.floor(rows/2))) - 1
    colIdx = 2*int(random.randint(1, math.floor(cols/2))) - 1

    return rowIdx, colIdx

def findVisitableCells(r, c, mazeT):
    shape = mazeT.shape
    
    visitableCells = []
    if (r - 2) > 0 and mazeT[r - 2, c] == 0:
        visitableCells.append(((r - 2, c), (r - 1, c)))
    if (c - 2) > 0 and mazeT[r, c-2] == 0:
        visitableCells.append(((r, c-2), (r, c-1)))
    if (r + 2) < (shape[0]-1) and mazeT[r + 2, c] == 0:
        visitableCells.append(((r+2, c), (r+1, c)))
    if (c + 2) < (shape[1]-1) and mazeT[r, c+2] == 0:
        visitableCells.append(((r, c+2), (r, c+1)))
    
    return visitableCells

def gen_maze(maze_no, rows=11, cols=11):
    mazeT = np.zeros((rows, cols), dtype=np.int32)
    start = getRandomEvenCoordinate(rows, cols)
    stack = [start]

    while len(stack) != 0:
        r, c = stack[-1]
        mazeT[r, c] = 1
        visitableCells = findVisitableCells(r, c, mazeT)
        if len(visitableCells) > 0:
            choice = random.choice(visitableCells)
            mazeT[choice[1]] = 1
            stack.append(choice[0])
        else:
            stack.pop()

    # Deepmind maze format
    entity_maze = ''
    for i in range(0, rows):
        for j in range(0, cols):

            if (i, j) == start:
                entity_maze += 'G'
            elif i > 0 and i < rows-1 \
                    and j > 0 and j < cols-1 \
                    and random.random() < .15:
                entity_maze += 'A'
            else:
                entity_maze += '*' if mazeT[i, j] == 0 else 'A'
            
        entity_maze += '\n'

    # Place spawn point
    entity_maze = entity_maze.replace('A', 'P', 1)

    # No variation for the moment
    #variation_maze = entity_maze.replace('P', 'A')
    #variation_maze = variation_maze.replace('G', 'A')
    #variation_maze = variation_maze.replace('A', ' ')

    
    # Voronoi points for intra-maze variation
    v_n = 8 if rows > 5 else 4
    v_pnts = []
    while len(v_pnts) < v_n:
        rc = getRandomEvenCoordinate(rows, cols)
        if rc not in v_pnts:
            v_pnts.append(rc)

    # Voronoi letters
    v_letters = []
    while len(v_letters) < v_n:
        letter = chr(ord('A') + random.randint(0, 25))
        if letter not in v_letters:
            v_letters.append(letter)

    # Populate the variation maze (can prolly be spedup significantly)
    variation_maze = ''
    for i in range(0, rows):
        for j in range(0, cols):
            variation_maze += v_letters[min_dist_index([i, j], v_pnts)]
        variation_maze += '\n' 
        
    return entity_maze[:-1], variation_maze[:-1]

def min_dist_index(x, Y):
    ret_ndx = -1
    dist = 100
    for i in range(0, len(Y)):
        euclid_norm = np.sqrt((Y[i][0]-x[0])**2 + (Y[i][1]-x[1])**2)
        if  euclid_norm < dist:
            dist = euclid_norm
            ret_ndx = i
    return ret_ndx



def load_pbs_template(template_file, searchpath="./"):
    """
    Uses jinja2 to load in a pbs template.
    """
    templateLoader = jinja2.FileSystemLoader(searchpath)
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template(template_file)
    return template


@click.command()
@click.option('--num_mazes', default=1000, help='Debug prompts')
@click.option('--template_file', default='random_map')
<<<<<<< 2357732be422b132ba38685930f88524693c69e9
@click.option('--store_dir', 
              default='/z/{}/implicit-mapping/deepmind-lab/assets/game_scripts'
             .format(os.environ['HOME']))
@click.option('--width', default=101)
@click.option('--height', default=101)
=======
@click.option('--mapdir', 
              default="/z/home/shurjo/implicit-mapping/maps")
@click.option('--width', default=5)
@click.option('--height', default=5)
>>>>>>> fix
@click.option('--debug', default=False)
def create_mazes(num_mazes, template_file, mapdir, width, height, debug):
    """
    Generates random mazes and their corresponding entity layers.
    """
    # Delete old maps
    subprocess.call("rm -rf /tmp/dmlab_level_data_0".split())

    # Set properties
    intra = True
    size = str(width) + 'x' + str(height)
    
    # dev null 
    if not debug:
        devnull = open(os.devnull, 'w')
    else:
        devnull = sys.stderr

    ################################################
    # Training
    ################################################
    
    # Map dir is based on height/width 
    map_dir = os.path.join(mapdir, "%02dx%02d" %(width, height), "training", "entityLayers")
    if not os.path.isdir(map_dir):
        os.makedirs(map_dir)
    
    # load in the pbs script
    for i in range(1, num_mazes+1):
        mapname = "%04d" %(i)
        print("Creating map: %s; " %mapname)
        
        # Generate random maze
        maze_entity, maze_var = gen_maze(maze_no=i, rows=height, cols=width)

        if debug:
            print("Entity Maze:\n%s" %maze_entity)
            print("Variation Maze:\b%s" %maze_var)
        
<<<<<<< 2357732be422b132ba38685930f88524693c69e9
        ################################################
        # Make the lua script to make the map
        ################################################
        os.chdir('/z/{}/implicit-mapping/make-random-maps'.format(os.environ['HOME']))
        

        lua_script = load_pbs_template(template_file +".lua")
        lua_exec = lua_script.render(maze_entity=maze_entity,
                                     maze_var=maze_var,
                                     template_file=template_file,
                                     maze_no=i, 
                                     mapname=mapname,
                                     numMaps=num_mazes,
                                     makeMap="true",
                                     time=.1,
                                     mapdir=mapdir)
        
        lua_filename = os.path.join(store_dir, "%s.lua" %mapname)
        with open(lua_filename, "w") as lua_file:
            lua_file.write(lua_exec)
        
=======
>>>>>>> fix
        #################################################
        ## Make the lua script to make the map
        #################################################
<<<<<<< 2357732be422b132ba38685930f88524693c69e9
        os.chdir('/z/{}/implicit-mapping/deepmind-lab'.format(os.environ['HOME']))
        p = subprocess.Popen("./compile_single_map.sh %s" %(mapname), 
                             stdout=devnull, 
                             stderr=devnull,shell=True)
        
        while not os.path.isfile(\
                '/tmp/dmlab_level_data_0/baselab/%s.map' %(mapname)):
            time.sleep(1)
            if p.poll():
                print("Map compilation terminated.")
                return

        # Kill bazel since it tends to get stuck
        subprocess.call("pkill -9 bazel".split())
        time.sleep(1)
=======
        #os.chdir('/z/home/shurjo/implicit-mapping/make-random-maps')
        #

        #lua_script = load_pbs_template(template_file +".lua")
        #lua_exec = lua_script.render(maze_entity=maze_entity,
        #                             maze_var=maze_var,
        #                             template_file=template_file,
        #                             maze_no=i, 
        #                             mapname=mapname,
        #                             numMaps=num_mazes,
        #                             makeMap="true",
        #                             time=.1,
        #                             mapdir=mapdir)
        #
        #lua_filename = os.path.join(store_dir, "%s.lua" %mapname)
        #with open(lua_filename, "w") as lua_file:
        #    lua_file.write(lua_exec)
        #
        ##################################################
        ### Compile the map files
        ##################################################
        #os.chdir('/z/home/shurjo/implicit-mapping/deepmind-lab')
        #p = subprocess.Popen("./compile_single_map.sh %s" %(mapname), 
        #                     stdout=devnull, 
        #                     stderr=devnull,shell=True)
        #
        #while not os.path.isfile(\
        #        '/tmp/dmlab_level_data_0/baselab/%s.map' %(mapname)):
        #    time.sleep(1)
        #    if p.poll():
        #        print("Map compilation terminated.")
        #        return

        ## Kill bazel since it tends to get stuck
        #subprocess.call("pkill -9 bazel".split())
        #time.sleep(1)

        ##################################################
        ### Copy the map files
        ##################################################
        #copyfile('/tmp/dmlab_level_data_0/baselab/%s.map' %mapname,
        #'/z/home/shurjo/implicit-mapping/deepmind-lab/assets/maps/%s.map' %(mapname))
>>>>>>> fix

        #################################################
        ## Overwrite the lua script (without map making)
        #################################################
<<<<<<< 2357732be422b132ba38685930f88524693c69e9
        copyfile('/tmp/dmlab_level_data_0/baselab/%s.map' %mapname,
        '/z' + os.environ['HOME'] + '/implicit-mapping/deepmind-lab/assets/maps/%s.map' %(mapname))

        ################################################
        # Overwrite the lua script (without map making)
        ################################################
        os.chdir('/z' + os.environ['HOME'] + '/implicit-mapping/make-random-maps')
        lua_script = load_pbs_template(template_file +".lua")
        lua_exec = lua_script.render(maze_entity=maze_entity,
                                     maze_var=maze_var,
                                     template_file=template_file,
                                     maze_no=i, 
                                     mapname=mapname,
                                     numMaps=num_mazes,
                                     makeMap="false",
                                     time=30,
                                     mapdir=mapdir)
        
        ################################################
        # Entity Layer 
        ################################################
        lua_filename = os.path.join(store_dir, "%s.lua" %mapname)
        with open(lua_filename, "w") as lua_file:
            lua_file.write(lua_exec)
=======
        #os.chdir('/z/home/shurjo/implicit-mapping/make-random-maps')
        #lua_script = load_pbs_template(template_file +".lua")
        #lua_exec = lua_script.render(maze_entity=maze_entity,
        #                             maze_var=maze_var,
        #                             template_file=template_file,
        #                             maze_no=i, 
        #                             mapname=mapname,
        #                             numMaps=num_mazes,
        #                             makeMap="false",
        #                             time=30,
        #                             mapdir=mapdir)
        #
        #################################################
        ## Entity Layer 
        #################################################
        #lua_filename = os.path.join(store_dir, "%s.lua" %mapname)
        #with open(lua_filename, "w") as lua_file:
        #    lua_file.write(lua_exec)
>>>>>>> fix

        # Generate corresponding entity layer
        entityLayer_script = load_pbs_template(template_file + ".entityLayer")
        entityLayer_exec = entityLayer_script.render(maze_entity=maze_entity)
        
        entityLayer_filename = os.path.join(map_dir, "%s.entityLayer" %mapname)
        with open(entityLayer_filename, "w") as entityLayer_file:
            entityLayer_file.write(entityLayer_exec)

        ################################################
        # Blank name layer 
        ################################################
        #copyfile('%s/%s.entityLayer' %(store_dir, mapname), 
        #         '%s/%s_blank_name.entityLayer' %(store_dir, mapname))
    
    
    ################################################
    # Testing 
    ################################################
    map_dir = os.path.join(mapdir, "%02dx%02d" %(width, height), "testing", "entityLayers")
    print(map_dir)
    if not os.path.isdir(map_dir):
        os.makedirs(map_dir)
    
    # load in the pbs script
    for i in range(1, int(round(num_mazes*0.2))+1):
        mapname = "%04d" %(i)
        print("Creating map: %s; " %mapname)
        
        # Generate random maze
        maze_entity, maze_var = gen_maze(maze_no=i, rows=height, cols=width)

        # Generate corresponding entity layer
        entityLayer_script = load_pbs_template(template_file + ".entityLayer")
        entityLayer_exec = entityLayer_script.render(maze_entity=maze_entity)
        
        entityLayer_filename = os.path.join(map_dir, "%s.entityLayer" %mapname)
        with open(entityLayer_filename, "w") as entityLayer_file:
            entityLayer_file.write(entityLayer_exec)



if __name__ == '__main__':
    create_mazes()
