from collections import deque
from copy import deepcopy
import sys
import random
import globalvars
from challenge_response import *


def create_event(eventid,nodeid,packetdetails,timeofevent):
    event = {'event_id':"DEFAULT", 'agent':0,'time':0}
    event['event_id'] = eventid
    event['agent'] = nodeid #agent creating the event
    event['time'] = timeofevent
    event['details'] = packetdetails
    
    

    return event


def update_assertion(claimant,prover,pos,conf,timeofpos,timeofevent):
    
    assertion = {'sender':"DEFAULT", 'agent':"DEFAULT",'position':(0,0,0), 'confidence':0,'timeofposition':0, 'timeofevent':0}
    assertion['sender'] = claimant
    assertion['agent'] = prover
    assertion['position'] = pos #of prover
    assertion['confidence'] = conf
    assertion['timeofposition'] = timeofpos
    assertion['timeofevent'] = timeofevent
    
    return assertion
 
 
def generateChallengeString(k):

    

    #Generate k-bit string starting and ending with 1's that act as sentinels
    S = "1"
    for i in range(k-2):
        x = random.randint(0, 1)
        S += str(x)

    S += "1"
     
    return S


def create_challenge(claimant,prover,challenger):
    
    challenge = {'prover':"DEFAULT", 'challenger':0,'time':0, 'challenge':"default challenge"}
    
    challenge['claimant'] = claimant #made the assertion about prover's position
    challenge['prover'] = prover
    challenge['challenger'] = challenger


    challenge['tau'] = 3 #seconds (TODO)
    k = random.randint(8, 16)
    challenge['challenge'] = generateChallengeString(k)
    
    return challenge
    

def start_timer(claimant,prover,node_id,timeofpos,duration):
    
    timer = {'prover':"DEFAULT", 'challenger':0, 'challenge':"default challenge"}
    
    timer['timer_claimant'] = claimant
    timer['timer_started_for'] = prover
    timer['timer_started_by'] = node_id
    timer['prover_pos_time'] = timeofpos
    timer['duration'] = duration
    
    return timer




def respond_to_challenge(tau):
    '''agent is turning flashlight on and off'''

    #incrementing the current time by the time it should take to perform the challenge-reponse
    #to indicate a successful response
    globalvars.now += tau


def node_handler(node_id,action,e,timeofevent):

#TODO multiple rounds need to be done
    if action == "SEND_PERIODIC_ASSERTION":
        #node_id is sending position claim
       # print("Agent ",node_id," is creating the packet for position claim at",globalvars.now, "seconds." )
        assertion = update_assertion(node_id,node_id,globalvars.pos[node_id],5,timeofevent,timeofevent)

        event_id = "ASSERTION_%03d" % (globalvars.idn)
        globalvars.idn += 1

        e = create_event(event_id,node_id,assertion,timeofevent)
        globalvars.event_queue.append(deepcopy(e))

        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])
        
  #  if action == "SEND_ASSERTION":
  #      #node_id is sending position claim
  #     # print("Agent ",node_id," is creating the packet for position claim at",globalvars.now, "seconds." )
  #      assertion = update_assertion(node_id,e['details']['prover'],globalvars.pos[e['details']['prover']],globalvars.confidence_table[node_id][e['details']['agent']],globalvars.now)

  #      event_id = "ASSERTION_%03d" % (globalvars.idn)
  #      globalvars.idn += 1

  #      e = create_event(event_id,node_id,assertion,globalvars.now)
  #      globalvars.event_queue.append(deepcopy(e))

  #      #sort queue according to the simulated real time (time of event happening)
  #      globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])
    
    if action == "SEND_CHALLENGE":
        #node_id is sending challenge
       # print("Agent ",node_id," is challenging e['details']['sender'] and creating the packet for challenge at",globalvars.now, "seconds." )
       

             
        challenge = create_challenge(e['details']['sender'],e['details']['agent'],node_id) #sender of assertion
        event_id = "CHALLENGE_%03d" % (globalvars.idn)

        timeofpos = e['details']['timeofposition']
        globalvars.idn += 1

        e = create_event(event_id,node_id,challenge,globalvars.now)
        globalvars.event_queue.append(deepcopy(e))

        #start timer event
        timer = start_timer(e['details']['claimant'],e['details']['prover'],node_id,timeofpos,challenge['tau'])
        event_id = "TIMERSTART_%03d" % (globalvars.idn)
        globalvars.idn += 1
        e = create_event(event_id,node_id,timer,globalvars.now)
        globalvars.event_queue.append(deepcopy(e))
        
        
        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])
        
        
    if action == "RESPOND_TO_CHALLENGE":
        #node_id will respond to challenge by turning on/off flashlight
        #respond_to_challenge(node_id,challenge)
        respond_to_challenge(e['details']['tau'])

        response = "yes"


        event_id = "RESPONSE_%03d" % (globalvars.idn)
        globalvars.idn += 1
        e = create_event(event_id,node_id,response,globalvars.now)
        globalvars.event_queue.append(deepcopy(e))
        
        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

        
    if action == "TIMER_EXPIRY":
        #node_id will do actions because of its own timer expiry
        #it verifies response, i.e., checks if prover's light is on and then increases/decreases confidence
        ret = is_success_response(e['details']['timer_started_for'])
        update_confidence(ret,e['details']['timer_started_for'],node_id,e['details']['timer_claimant'],e)
        update_trust(ret,e['details']['timer_started_for'],node_id,e['details']['timer_claimant'])

        timeofevent = e['time']+e['details']['duration']
        timeofpos = e['details']['prover_pos_time']
        if globalvars.max_reached == 1:
            assertion = update_assertion(node_id,e['details']['timer_started_for'],globalvars.pos[e['details']['timer_started_for']],globalvars.confidence_table[node_id][e['details']['timer_started_for']],timeofpos,timeofevent)

            event_id = "ASSERTION_%03d" % (globalvars.idn)
            globalvars.idn += 1

            e = create_event(event_id,node_id,assertion,globalvars.now)
            globalvars.event_queue.append(deepcopy(e))

            #sort queue according to the simulated real time (time of event happening)
            globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

        
        
  
def is_success_response(agent):
        return 1


def update_confidence(success,prover,agent,claimant,e):

    
    if success == 1:#direct verification success
        if globalvars.confidence_table[agent][prover]!=5:
            globalvars.confidence_table[agent][prover] = 5
            globalvars.max_reached += 1
        #node_handler(agent,"SEND_ASSERTION",e)

    if success == 0:#direct verification failure
        globalvars.confidence_table[agent][prover] -= globalvars.confidence_table[claimant][prover]*globalvars.trust_table[agent][claimant]*check_verifiability(agent,prover)

def update_trust(success,prover,agent,claimant):
     if success == 1:#direct verification success
        globalvars.trust_table[agent][claimant] += 1
        globalvars.trust_table[agent][claimant] = (globalvars.trust_table[agent][claimant]-0)/(5-0)




def calc_distance(i,j):

    import math
    import numpy as np

    '''calculating distance between  agent i and j'''

    p = np.array([globalvars.pos[i][0],globalvars.pos[i][1],globalvars.pos[i][2]])
    q = np.array([globalvars.pos[j][0],globalvars.pos[j][1],globalvars.pos[j][2]])
    print(p)
    print(q)
    d = np.linalg.norm(p-q) 
    print(d) 

    #convert to feet
    d = d*100
    return d


def is_in_direct_view(agent1,agent2):
    #find the equation of the line segment joining agent1 and agent2

    #Find the DR’s (Direction Ratios) by taking the difference of the corresponding position coordinates of the two given points. l = (x2 – x1), m = (y2 – y1), n = (z2 – z1); Here l, m, n are the DR’s.

    l = abs(globalvars.pos[agent2][0]-globalvars.pos[agent1][0])
    m = abs(globalvars.pos[agent2][1]-globalvars.pos[agent1][1])
    n = abs(globalvars.pos[agent2][2]-globalvars.pos[agent1][2])
    print("l",l) 
    print("m",m) 
    print("n",n) 
    

    #print("Direction ratios:",l,m,n)
    #Choose either of the two given points say, we choose (x1, y1, z1).
    #Write the required equation of the straight line passing through the points (x1, y1, z1) and (x2, y2, z2). L : (x – x1)/l = (y – y1)/m = (z – z1)/n

       
    #check with all other points if they lie on the line segment
    for i in range(globalvars.number_of_nodes):
        if i != agent2 and i != agent1:
            print("third point is ",globalvars.pos[i])
            if l>0 and m>0 and n>0:
                a = abs(globalvars.pos[i][0]-globalvars.pos[agent1][0])/l
                b = abs(globalvars.pos[i][1]-globalvars.pos[agent1][1])/m
                c = abs(globalvars.pos[i][2]-globalvars.pos[agent1][2])/n
                print("a=",a)
                print("b=",b)
                print("c=",c)
                if a == b and b == c:
                    return 0 #not in direct view, some point is blocking
                else:
                    continue

            if l == 0 and m>0 and n>0:
                b = abs(globalvars.pos[i][1]-globalvars.pos[agent1][1])/m
                c = abs(globalvars.pos[i][2]-globalvars.pos[agent1][2])/n
                print("c=",c)
                print("b=",b)
                if b == c and globalvars.pos[i][0] == globalvars.pos[agent1][0] and globalvars.pos[i][0] == c:
                    return 0
                else:
                    continue
            
            if l > 0 and m == 0 and n>0:
                a = abs(globalvars.pos[i][0]-globalvars.pos[agent1][0])/l
                c = abs(globalvars.pos[i][2]-globalvars.pos[agent1][2])/n
                print("a=",a)
                print("c=",c)
                if a == c and globalvars.pos[i][1] == globalvars.pos[agent1][1] and globalvars.pos[agent1][1] == c:
                    return 0
                else:
                    continue

            if l > 0 and m > 0 and n == 0:
                a = abs(globalvars.pos[i][0]-globalvars.pos[agent1][0])/l
                b = abs(globalvars.pos[i][1]-globalvars.pos[agent1][1])/m
                print("a=",a)
                print("b=",b)

                if b == a and globalvars.pos[i][2] == globalvars.pos[agent1][2] and globalvars.pos[agent1][1] == a:
                    return 0
                else:
                    continue

            #if it is one of the axes
            if l == 0 and m == 0: #z-axis
                if  (globalvars.pos[agent2][2] < globalvars.pos[i][2] < globalvars.pos[agent1][2] or globalvars.pos[agent1][2] < globalvars.pos[i][2] < globalvars.pos[agent2][2]) and (globalvars.pos[i][1] == 0) and (globalvars.pos[i][0] == 0):
                    return 0
                else:
                    continue
            if l == 0 and n == 0: #y-axis
                if  (globalvars.pos[agent2][1] < globalvars.pos[i][1] < globalvars.pos[agent1][1] or globalvars.pos[agent1][1] < globalvars.pos[i][1] < globalvars.pos[agent2][1]) and (globalvars.pos[i][0] == 0) and (globalvars.pos[i][2] == 0):
                    return 0
                else:
                    continue
            if n == 0 and m == 0: #x-axis
                if  (globalvars.pos[agent2][0] < globalvars.pos[i][0] < globalvars.pos[agent1][0] or globalvars.pos[agent1][0] < globalvars.pos[i][0] < globalvars.pos[agent2][0]) and (globalvars.pos[i][1] == 0) and (globalvars.pos[i][2] == 0):
                    return 0
                else:
                    continue




    return 1 #is in direct view


def check_verifiability(agent1,agent2):

    #V(d)
    #check field of view

    ret = is_in_direct_view(agent1,agent2)
    
    verifiability = 0
    p = np.array([globalvars.pos[agent1][0],globalvars.pos[agent1][1],globalvars.pos[agent1][2]])
    q = np.array([globalvars.pos[agent2][0],globalvars.pos[agent2][1],globalvars.pos[agent2][2]])
    print(p)
    print(q)
 
    if ret == 1:
        #check distance
        #minimum distance between agents = 100 feet
        thres1 = 100 #feet
        thres2 = 500 #feet

        d = calc_distance(agent1, agent2)

        print("Distance (feet)=",d)
        if d <= thres1:
            verifiability = 1
        elif d >= thres2:
            verifiability = 0
        else:
            verifiability = 1 - ((d-thres1)/(thres2-thres1))
        
        print("Agents ",agent1,"and",agent2," are in direct view; Verifiability = ",verifiability)
    else:
        print("Agents ",agent1,"and",agent2," are NOT in direct view; Verifiability = ",verifiability)

    return verifiability
   
def process_event(e):

    if "ASSERTION" in e['event_id']:
        #send challenge for each position claim from each agent that received the claim
        #increment simulation time
        globalvars.now += globalvars.e_now 

        for i in range(globalvars.number_of_nodes): #everyone received because wireless communication is infinite
            if e['agent'] != i:
                ret = check_verifiability(e['agent'],i) #TODO should take position from the assertion. Right now for the all-honest case it is fine.
                dist = calc_distance(e['agent'],i)
                transmission_delay = 0.008 #seconds
                dist = 0.3048*100*dist
                propagation_delay = dist/globalvars.speed
                timeofevent = e['time'] + transmission_delay + propagation_delay
                if ret > 0:
                    node_handler(i,"SEND_CHALLENGE",e,timeofevent)
                if ret == 0:
                    delta=(timeofevent-e['time'])/10
                    prev = globalvars.confidence_table[i][e['details']['agent']]
                    globalvars.confidence_table[i][e['details']['agent']] +=  (globalvars.confidence_table[i][e['details']['agent']])/ (delta+1) + globalvars.trust_table[i][e['details']['sender']]*globalvars.confidence_table[e['details']['sender']][e['details']['agent']]
                    if globalvars.confidence_table[i][e['details']['agent']] > prev:
                        #add assertion event in node_handler TODO
                        assertion = update_assertion(i,e['details']['agent'],globalvars.pos[e['details']['agent']],globalvars.confidence_table[i][e['details']['agent']],e['details']['timeofposition'],timeofevent)

                        event_id = "ASSERTION_%03d" % (globalvars.idn)
                        globalvars.idn += 1

                        e = create_event(event_id,i,assertion,timeofevent)
                        globalvars.event_queue.append(deepcopy(e))

                        #sort queue according to the simulated real time (time of event happening)
                        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

                        #node_handler(i,"SEND_ASSERTION",e)



    if "CHALLENGE" in e['event_id']:
        #turn on flashlight for all the agents who got the challenge
        globalvars.now += globalvars.e_now

        print("event:",e)
        timeofevent = e['time']+ e['details']['tau']  
        for i in range(globalvars.number_of_nodes):
            if e['details']['prover'] == i:
                node_handler(i,"RESPOND_TO_CHALLENGE",e,timeofevent)
                
                
    if "TIMERSTART" in e['event_id']:
        #create a timer expiry event for every timerstart event
        timeofevent = e['time']+ e['details']['duration'] 
        node_handler(e['details']['timer_started_by'],"TIMER_EXPIRY",e,timeofevent)
        
def make_confidence_table(): 
    from collections import defaultdict
    from itertools import permutations 
   # confidence_table = defaultdict(dict)

    for (my_id, other) in permutations(range(globalvars.number_of_nodes), 2):
        globalvars.confidence_table[my_id][other] = 0
        globalvars.confidence_table[my_id][my_id] = 5



def make_trust_table(): 
    from collections import defaultdict
    from itertools import permutations 
   # confidence_table = defaultdict(dict)

    for (my_id, other) in permutations(range(globalvars.number_of_nodes), 2):
        globalvars.trust_table[my_id][other] = 0
        globalvars.trust_table[my_id][my_id] = 999


def extract_confidence_from_database(agent_id):

    print("Confidence table (Agent ID: Confidence) for agent ", agent_id)
    print(globalvars.confidence_table[agent_id])


def read_file(pos_file):

    import ast

    f=open(pos_file,mode='r')
    lines =  f.read()
    f.close()
    return lines


def main():
    '''Simulation engine'''
    
    #cparse argumentd
    if len(sys.argv) < 3:
        print("Usage: simulator_engine.py <number of nodes>")
        sys.exit();
    
    globalvars.init()
    globalvars.number_of_nodes = int(sys.argv[1])
    testcase = int(sys.argv[2])
    print("Number of agents = ", globalvars.number_of_nodes)

    #create agent positions
    filename = "pos_%d.txt" % (testcase)
    globalvars.pos = eval(read_file(filename))
    print(globalvars.pos)
    
    #create confidence table
    make_confidence_table()
    make_trust_table()
    
    #extract_confidence_from_database(0)
    #sys.exit()
    #add first event(s) to the event_queue
    e = {'event_id':"DEFAULT", 'agent':0,'time':0}
    for i in range(globalvars.number_of_nodes):
        node_handler(i,"SEND_PERIODIC_ASSERTION",e,0);
        
    print("Initial events:")
    print(*globalvars.event_queue,sep="\n")
    
    #process event queue
    while globalvars.event_queue:
        item = globalvars.event_queue.pop(0)
        print("\nEvent occuring: ",item)
        process_event(item)
        print("\nconfidence_table\n")
        print(globalvars.confidence_table)
        print("\ntrust_table\n")
        print(globalvars.trust_table)

        print("\nEVENT QUEUE:\n")
        print("-----------------")
        print(*globalvars.event_queue,sep="\n")



    print("confidence_table")
    print(globalvars.confidence_table)
    print("trust_table")
    print(globalvars.trust_table)



if __name__=="__main__":
    main()
