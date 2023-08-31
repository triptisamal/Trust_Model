from collections import deque
from copy import deepcopy
import sys
import random
import globalvars
from challenge_response import *

def write_to_file(filename,content):
    
    original_stdout = sys.stdout
    with open(filename,'a') as f:
        sys.stdout = f
        print(content)
    sys.stdout = original_stdout



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


def create_challenge(claimant,prover,challenger,position,position_time):
    
    challenge = {'prover':"DEFAULT", 'challenger':0,'time':0, 'challenge':"default challenge", 'position':(0,0,0), 'time_of_position':0}
    
    challenge['claimant'] = claimant #made the assertion about prover's position
    challenge['prover'] = prover
    challenge['challenger'] = challenger


    challenge['tau'] = 3 #seconds (TODO)
    k = random.randint(8, 16)
    challenge['challenge'] = generateChallengeString(k)
    challenge['position'] = position
    challenge['time_of_position'] = position_time
    
    return challenge
    

def start_timer(claimant,prover,node_id,timeofpos,pos,duration):
    
    timer = {'timer_claimant':"DEFAULT",'timer_started_for':"DEFAULT", 'timer_started_by':0, 'prover_pos_time':0,'duration':0}
    
    timer['timer_claimant'] = claimant
    timer['timer_started_for'] = prover
    timer['timer_started_by'] = node_id
    timer['prover_pos_time'] = timeofpos
    timer['position'] = pos
    timer['duration'] = duration
    
    return timer




def respond_to_challenge(tau):
    '''agent is turning flashlight on and off'''

    #incrementing the current time by the time it should take to perform the challenge-reponse
    #to indicate a successful response
    globalvars.now += tau

    return 1


def node_handler(node_id,action,e,timeofevent):
    
    if action == "UPDATE_DATABASE":
        print_database(node_id,timeofevent)
        event_id = "DATABASE_%03d" % (globalvars.idn)
        globalvars.idn += 1
        update = "DB is updated"
        e = create_event(event_id,node_id,update,timeofevent)
        globalvars.event_queue.append(deepcopy(e))

        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])


    if action == "SEND_PERIODIC_ASSERTION":

        #node_id is sending position claim
       # print("Agent ",node_id," is creating the packet for position claim at",globalvars.now, "seconds." )
        assertion = update_assertion(node_id,node_id,globalvars.pos[node_id],globalvars.direct_verification_score,timeofevent,timeofevent)

        event_id = "ASSERTION_%03d" % (globalvars.idn)
        globalvars.idn += 1

        e = create_event(event_id,node_id,assertion,timeofevent)
        globalvars.event_queue.append(deepcopy(e))

        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])
        
    
    if action == "SEND_AND_RECEIVE_CHALLENGE":
        #node_id is sending challenge
             
        challenge = create_challenge(e['details']['sender'],e['details']['agent'],node_id,e['details']['position'],e['details']['timeofposition']) #sender of assertion
        event_id = "CHALLENGE_%03d" % (globalvars.idn)

        timeofpos = e['details']['timeofposition']
        globalvars.idn += 1
        

        e = create_event(event_id,node_id,challenge,globalvars.now)# TODO this is the time challenge was received by the receiver agent
       # e = create_event(event_id,node_id,challenge,timeofevent)# this is the time challenge was received by the receiver agent
        globalvars.event_queue.append(deepcopy(e))

        #start timer event
        timer = start_timer(e['details']['claimant'],e['details']['prover'],node_id,timeofpos,e['details']['position'],challenge['tau'])
        event_id = "TIMERSTART_%03d" % (globalvars.idn)
        globalvars.idn += 1
        e = create_event(event_id,node_id,timer,globalvars.now) # TODO this is the time at which timer was started at the sending agent
        #e = create_event(event_id,node_id,timer,timeofevent) # this is the time at which timer was started at the sending agent
        globalvars.event_queue.append(deepcopy(e))
        
        
        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])
        
        
    if action == "RESPOND_TO_CHALLENGE":
        #node_id will respond to challenge by turning on/off flashlight
        #respond_to_challenge(node_id,challenge)
        ret = respond_to_challenge(e['details']['tau'])

        if ret == 1:
            response = "Responding"
        
        event_id = "RESPONSE_%03d" % (globalvars.idn)
        globalvars.idn += 1
        e = create_event(event_id,node_id,response,globalvars.now)#TODO timeofevent is the time at which agent will have successfully performed the challenge
        #e = create_event(event_id,node_id,response,timeofevent)#timeofevent is the time at which agent will have successfully performed the challenge
        globalvars.event_queue.append(deepcopy(e))
        
        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

        
    if action == "TIMER_EXPIRY":
        #node_id will do actions because of its own timer expiry
        #it verifies response, then increases/decreases confidence

        ret = is_success_response(e['details']['timer_started_for'])
        conf = update_confidence(ret,e['details']['timer_started_for'],node_id,e['details']['timer_claimant'],e,timeofevent)

        timeofevent = e['time']+e['details']['duration']
        timeofpos = e['details']['prover_pos_time']
        
        
  
def is_success_response(agent):
        return 1


def update_confidence(success,prover,agent,claimant,e,timeofevent):

    
    if success == 1:#direct verification success
        confidence = globalvars.direct_verification_score
        update_database(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
        print("AGENT ",agent,": Updating confidence in position of agent ",prover," based on direct verification.")
        print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])


    if success == 0:#direct verification failure
        confidence = 0
        update_database(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
        print("AGENT ",agent,": Updating confidence in position of agent ",prover," based on direct verification.")
        print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])

    return confidence



def calc_distance(i,j):

    import math
    import numpy as np

    '''calculating distance between  agent i and j'''

    p = np.array([globalvars.pos[i][0],globalvars.pos[i][1],globalvars.pos[i][2]])
    q = np.array([globalvars.pos[j][0],globalvars.pos[j][1],globalvars.pos[j][2]])
 #   print(p)
  #  print(q)
    d = np.linalg.norm(p-q) 
   # print(d) 

    #convert to feet
    d = d*100
    return d


def is_in_direct_view(agent1,agent2):
    #agent 1 is actually the same position as event['details']['position']


    #find the equation of the line segment joining agent1 and agent2

    #Find the DR’s (Direction Ratios) by taking the difference of the corresponding position coordinates of the two given points. l = (x2 – x1), m = (y2 – y1), n = (z2 – z1); Here l, m, n are the DR’s.

    l = abs(globalvars.pos[agent2][0]-globalvars.pos[agent1][0])
    m = abs(globalvars.pos[agent2][1]-globalvars.pos[agent1][1])
    n = abs(globalvars.pos[agent2][2]-globalvars.pos[agent1][2])
 #   print("l",l) 
 #   print("m",m) 
 #   print("n",n) 
 #   

    #print("Direction ratios:",l,m,n)
    #Choose either of the two given points say, we choose (x1, y1, z1).
    #Write the required equation of the straight line passing through the points (x1, y1, z1) and (x2, y2, z2). L : (x – x1)/l = (y – y1)/m = (z – z1)/n

       
    #check with all other points if they lie on the line segment
    for i in range(globalvars.number_of_nodes):
        if i != agent2 and i != agent1:
         #   print("third point is ",globalvars.pos[i])
            if l>0 and m>0 and n>0:
                a = abs(globalvars.pos[i][0]-globalvars.pos[agent1][0])/l
                b = abs(globalvars.pos[i][1]-globalvars.pos[agent1][1])/m
                c = abs(globalvars.pos[i][2]-globalvars.pos[agent1][2])/n
 #               print("a=",a)
 #               print("b=",b)
 #               print("c=",c)
                if a == b and b == c:
                    return 0 #not in direct view, some point is blocking
                else:
                    continue

            if l == 0 and m>0 and n>0:
                b = abs(globalvars.pos[i][1]-globalvars.pos[agent1][1])/m
                c = abs(globalvars.pos[i][2]-globalvars.pos[agent1][2])/n
         #       print("c=",c)
         #       print("b=",b)
                if b == c and globalvars.pos[i][0] == globalvars.pos[agent1][0] and globalvars.pos[i][0] == c:
                    return 0
                else:
                    continue
            
            if l > 0 and m == 0 and n>0:
                a = abs(globalvars.pos[i][0]-globalvars.pos[agent1][0])/l
                c = abs(globalvars.pos[i][2]-globalvars.pos[agent1][2])/n
         #       print("a=",a)
         #       print("c=",c)
                if a == c and globalvars.pos[i][1] == globalvars.pos[agent1][1] and globalvars.pos[agent1][1] == c:
                    return 0
                else:
                    continue

            if l > 0 and m > 0 and n == 0:
                a = abs(globalvars.pos[i][0]-globalvars.pos[agent1][0])/l
                b = abs(globalvars.pos[i][1]-globalvars.pos[agent1][1])/m
         #       print("a=",a)
         #       print("b=",b)

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
 
    if ret == 1:
        #check distance
        #minimum distance between agents = 100 feet
        thres1 = 100 #feet
        thres2 = 500 #feet

        d = calc_distance(agent1, agent2)

        if d <= thres1:
            verifiability = 1
        elif d >= thres2:
            verifiability = 0
        else:
            verifiability = 1 - ((d-thres1)/(thres2-thres1))
        
        print("SIMULATOR: Agents ",agent1,"and",agent2," are in direct view; Verifiability = ",verifiability)
    else:
        print("SIMULATOR: Agents ",agent1,"and",agent2," are NOT in direct view; Verifiability = ",verifiability)

    return verifiability


def update_database(my_id,prover,sender,position,timeofposition,confidence,current_time):

    globalvars.flag = 1
    #tup = (x, y, z, s, t, c) x = agent whose database this is, y = agent whose position is in database, z = position of y, s= sender of assertion, t = time of position,
    

    self_id = my_id
    y = prover 
    z = position 
    s = sender 
    t = timeofposition
    c = confidence
    globalvars.database[self_id][prover] = {}

    #globalvars.database[self_id]['prover'] = prover 
    globalvars.database[self_id][prover]['position'] = position 
    globalvars.database[self_id][prover]['sender'] = sender 
    globalvars.database[self_id][prover]['time_of_position'] = timeofposition 
    globalvars.database[self_id][prover]['confidence'] = confidence 
    globalvars.database[self_id][prover]['update_time'] = current_time 

   # tup = (x,y,z,s,t,c)
    #globalvars.database.append(tup)
      

def check_database(my_id,other_agent,assertion_pos):

    if not globalvars.database:
        return 0
    else:
        for key, value in globalvars.database.items():#myid
            if key == my_id:
                for ky, val in globalvars.database[key].items():#otheragent
                    if ky == other_agent:
                        for k, v in database[key][ky].items():
                            if k == 'position' and v == assertion_pos:
                                return globalvars.database[key][ky]['confidence']

    return 0

def print_database(agent_id,event_time):
    
    #decay of ALL the confidence values that agent_id has stored
    if globalvars.database:
        for key, value in globalvars.database.items():
            for ky, val in globalvars.database[key].items():
               for k, v in globalvars.database[key][ky].items():
                    if k == 'update_time' and event_time < globalvars.database[key][ky]['update_time']:#to account for database_update event that happened before challenge response
                        break
                    else:
                        if k == 'confidence':
                            globalvars.database[key][ky]['confidence'] = globalvars.database[key][ky]['confidence'] - globalvars.delta*(event_time-globalvars.database[key][ky]['update_time'])
                            globalvars.database[key][ky]['update_time'] = event_time
        
                            #print the database
                            for i, j in globalvars.database.items():
                                print("SIMULATOR: Database at time ",event_time," for agent",i,":", j)
                        else:
                            continue


    contents = "%s at time %d\n" % (globalvars.database, event_time)
    write_to_file("database.txt",contents)
        #write_to_file("database.txt",globalvars.database)



def process_event(e):
    
    #Everytime an event is processed, print the database
    if "DATABASE" in e['event_id']:
        
        #only add new actions if there are no more ASSERTION events
        ret = 0
        ret = check_event_queue()
        ret = 1
        if ret:
            #generate another database update
           #set granularity
           # timeofevent = e['time']+1
            timeofevent = e['time']+2
            print("e['time']=",e['time'])
            #Trigger database refresh for all agents
            #for i in range(globalvars.number_of_nodes):
            node_handler(0,"UPDATE_DATABASE",e,timeofevent)



    if "ASSERTION" in e['event_id']:
        #send challenge for each position claim from each agent that received the claim
        #increment simulation time
        globalvars.now += globalvars.e_now 

        for i in range(globalvars.number_of_nodes): #everyone received because wireless communication is infinite
            if e['agent'] != i:#e['agent'] is making the assertion

                ret = check_verifiability(e['details']['agent'],i) 
                dist = calc_distance(e['agent'],i)
                transmission_delay = 0.008 #seconds
                dist = 0.3048*100*dist
                propagation_delay = dist/globalvars.speed
                timeofevent = e['time'] + transmission_delay + propagation_delay
                #at timeofevent challenge will be received at i

                if ret > 0:
                    #it is verifiable, i.e. direct verification is possible
                    print("AGENT ",i,": Can directy verify the position of agent ",e['agent'])
                    
                    #if challenge not done yet or if the confidence is less than cf_min (Confidence Threshold)
                    #check database to find what the previous confidence is if already received an assertion for the same position
                    confidence = check_database(i,e['agent'],e['details']['position']) 
                    if confidence < globalvars.cf_min:
                        node_handler(i,"SEND_AND_RECEIVE_CHALLENGE",e,timeofevent)
                   
                    

    if "CHALLENGE" in e['event_id']:
        #turn on flashlight for all the agents who got the challenge
        globalvars.now += globalvars.e_now

        print("SIMULATOR: Event:",e)
        timeofevent = e['time']+ e['details']['tau']  
        for i in range(globalvars.number_of_nodes):
            if e['details']['prover'] == i:
                node_handler(i,"RESPOND_TO_CHALLENGE",e,timeofevent)
                
                
    if "TIMERSTART" in e['event_id']:
        #create a timer expiry event for every timerstart event
        print("SIMULATOR: Event:",e)
        timeofevent = e['time']+ e['details']['duration'] 
        node_handler(e['details']['timer_started_by'],"TIMER_EXPIRY",e,timeofevent)
    



#def make_database(): 
#
#    tup = (999999,9999,9999,999,999)
#
#    for i in range(globalvars.number_of_nodes)
#    globalvars.database.append(tup)
#    print(globalvars.database)



def make_confidence_table(current_time): 
    from collections import defaultdict
    from itertools import permutations 
   # confidence_table = defaultdict(dict)
    
    if current_time == 0:
        for (my_id, other) in permutations(range(globalvars.number_of_nodes), 2):
            globalvars.confidence_table[my_id][other] = 0
            globalvars.confidence_table[my_id][my_id] = globalvars.direct_verification_score
    else:
        for (my_id, other) in permutations(range(globalvars.number_of_nodes), 2):
            globalvars.confidence_table[my_id][other] = (globalvars.confidence_table[my_id][other])-globalvars.delta*(current_time)
            globalvars.confidence_table[my_id][my_id] = globalvars.direct_verification_score


def make_trust_table(): 
    from collections import defaultdict
    from itertools import permutations 
   # confidence_table = defaultdict(dict)

    for (my_id, other) in permutations(range(globalvars.number_of_nodes), 2):
        globalvars.trust_table[my_id][other] = 0
        globalvars.trust_table[my_id][my_id] = 999


def extract_confidence_from_database(agent_id):

    print("Confidence table (Agent ID: Confidence) for agent ", agent_id)
    #print(globalvars.confidence_table[agent_id])


def read_file(pos_file):

    import ast

    f=open(pos_file,mode='r')
    lines =  f.read()
    f.close()
    return lines

def check_event_queue():

    for e in globalvars.event_queue:
        if "ASSERTION" in e['event_id'] or "CHALLENGE" in e['event_id'] or "TIMERSTART" in e['event_id']:
            return 1
    return 0



def main():
    '''Simulation engine'''
    
    #cparse argumentd
    if len(sys.argv) < 3:
        print("Usage: simulator_engine.py <number of nodes> <testcase number>")
        sys.exit();
    
    globalvars.init()
    globalvars.number_of_nodes = int(sys.argv[1])
    testcase = int(sys.argv[2])
 #   globalvars.delta = float(sys.argv[3])
 #   globalvars.refresh_period = int(sys.argv[4])
 #   globalvars.direct_verification_score = int(sys.argv[5])


   # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print("\nSIMULATOR ENGINE")
    #print("===========================")
    print("SIMULATOR: Number of agents = ", globalvars.number_of_nodes)

    #create agent positions
    filename = "pos_%d.txt" % (testcase)
    globalvars.pos = eval(read_file(filename))
    print("SIMULATOR: position of all agents: ",globalvars.pos)
    
    #create confidence table
    #TODO remove this part of code and add to 5-tuple
    #make_confidence_table(0)


    #make_database()
    #make_trust_table()
    
    #add first event(s) to the event_queue
    e = {'event_id':"DEFAULT", 'agent':0,'time':0}
    for i in range(globalvars.number_of_nodes):
        node_handler(i,"SEND_PERIODIC_ASSERTION",e,0);
    node_handler(0,"UPDATE_DATABASE",e,0);
        #node_handler(i,"SEND_PERIODIC_ASSERTION",e,globalvars.refresh_period);
        #node_handler(i,"SEND_PERIODIC_ASSERTION",e,2*globalvars.refresh_period);

        
    print("SIMULATOR: Initial events:")
    print(*globalvars.event_queue,sep="\n")
    print("===============================================================================\n\n\n")
    

    decaying=0 #timeofevent
    #process event queue
    while globalvars.event_queue:
        item = globalvars.event_queue.pop(0)
        process_event(item)

        print("\nSIMULATOR: Event processed: ",item)
        print("\nSIMULATOR: Time of the Event: ",item['time'])

        print("\nSIMULATOR: EVENT QUEUE:\n")
        print("-----------------")
        print(*globalvars.event_queue,sep="\n")
        print("===============================================================================\n\n\n")



    #print("SIMULATOR: End: confidence_table")
    #print(globalvars.confidence_table)
    #print("SIMULATOR: End: trust_table")
    #print(globalvars.trust_table)
    print("SIMULATOR: End: database")
    print(globalvars.database)



if __name__=="__main__":
    main()
