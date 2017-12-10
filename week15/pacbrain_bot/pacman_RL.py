import time
import random
import curses

import pac_world
import draw_pac
import feature
import bot_comm

alpha = 0.25#0.05
gamma = 0.9

step_display_time = .20

if bot_comm.ser:
    step_display_time = 0#2.5#

def main(scr):
    curses.curs_set(0)
    draw_pac.init_color()

    pWorld = pac_world.Pacworld()
    fVector = feature.get_default_vector()

    for i in range(1):

        pWorld.draw_world(scr)
        feature.render_fvector(scr, fVector)
        scr.addstr(1, 22 + i, "?", curses.A_REVERSE)
        scr.addstr(2, 30,"Game %d  " % (i + 1) )
        scr.refresh()
        time.sleep(1)

        fvector, succ = pacman_game(scr, pWorld, fVector)
        if succ:
            scr.addstr(1, 22 + i, "X", draw_pac.CP_R_EYES)
        else:
            scr.addstr(1, 22 + i, "X", draw_pac.CP_G_EYES)
        pWorld.reset(False)

    for i in range(15, 0, -1):
        scr.addstr(0, 25, 'Closing in %i seconds!!!!  ' % i)
        scr.refresh()
        time.sleep(1)
 
    exit() 

def Q_vector(fVector, result, world):

    res_Q = []

    for i in range( len(fVector) ):
        weight = fVector[i]
        func = feature.feature_func[i]
        res_Q.append( weight * func(result, world) )

    return res_Q

def pacman_game(scr, pWorld, fVector):

    complete = False

    reward = 0

    #While we haven't won yet
    while not complete:
        """
        Step 1:
        For our current state, check all the Q values (for each action a)
        """
        #Given a Q value, which A value gave us that?
        Q_to_A = {}
        #A list of all our Q values
        Q_list = []
        #Given an action, what was the result?
        result_dict = {}

        for curr_a in pWorld.pac_actions():
            result = pWorld.predict_state(curr_a)

            Q_vec = Q_vector(fVector, result, pWorld)
            Q = sum(Q_vec)

            #scr.addstr(15 + curr_a, 22, "%d : %.2f + %.2f + %.2f = %.2f" % (curr_a, Q_vec[0], Q_vec[1], Q_vec[2], Q) )

            Q_list.append(Q)
            Q_to_A[ Q ] = curr_a
            result_dict[curr_a] = result

            #scr.addstr(15 + curr_a, 22, "%d : %.2f" % (curr_a, Q) )
        """
        Step 2:
        Select the a which produces the highest Q
        """
        chosen_Q = max(Q_list)
        chosen_a = Q_to_A[ chosen_Q ]
        chosen_result = result_dict[chosen_a]        

        """
        Step 3: Take that action
        Step 4: Calculate the reward of our new state
        """
        complete, reward = pWorld.do_step(scr, chosen_a)

        """
        Step 5: 
        Using the reward, calculate the difference
        """
        #A list of our all the Q values for our new state
#        Q_list = []
#        for curr_a in pac_world.action_list:
#            result = pWorld.predict_state(curr_a)
#
#            Q = sum( Q_vector(fVector, result, pWorld) )
#
#            Q_list.append(Q)
#
#        diff = ( reward + gamma * max( Q_list ) ) - chosen_Q

        """
        Step 6:
        Adjust the weights of our weight vector
        """
        #for i in range( len(fVector) ):
        #    weight = fVector[i]
        #    func = feature.feature_func[i]

        #    fVector[i] = weight + alpha * diff * func(chosen_result, pWorld)

        """
        Step 7:
        Update our display
        """
        feature.render_fvector(scr, fVector)
        scr.refresh()
        time.sleep(step_display_time)

    success = False

    if reward >= 0:
        scr.addstr(0, 30,"Pacman Wins!!! ", draw_pac.CP_R_EYES)
        success = True
    else:
        scr.addstr(0, 30,"Pacman Loses!!!", draw_pac.CP_G_EYES)

    scr.refresh()
    time.sleep(2)

    scr.addstr(0, 30, " " * 15)

    return fVector, success

curses.wrapper(main)


