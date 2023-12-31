from collections import deque
from copy import deepcopy
import sys
import random
from itertools import permutations
import threading
import csv

from network_create import *
import globalvars


def write_to_file(filename,content):
    
    original_stdout = sys.stdout
    with open(filename,'a') as f:
        sys.stdout = f
        print(content)
    sys.stdout = original_stdout


def read_file(pos_file):

    import ast

    f=open(pos_file,mode='r')
    lines =  f.read()
    f.close()
    return lines

        

def update_assertiondatabase(self_id,other_id,sender,position,timeofposition,confidence,current_time):

    tup = {}
    tup['my_id'] = self_id #agent whose database this is 
    tup['other_id'] = other_id #agent whose position information is saved in this tuple 
    tup['position'] = position #position
    tup['sender'] = sender #agent who made the position assertion
    tup['time_of_position'] = timeofposition #time of position

    globalvars.assertion.append(tup)


def update_confdatabase(my_id,other_id,sender,position,timeofposition,confidence,current_time):

    self_id = my_id
    globalvars.database[self_id][other_id] = {}

    globalvars.database[self_id][other_id]['position'] = position 
    globalvars.database[self_id][other_id]['time_of_position'] = timeofposition 
    globalvars.database[self_id][other_id]['confidence'] = confidence 
    globalvars.database[self_id][other_id]['update_time'] = current_time 
    

    print_database(current_time)
    
def update_position_in_database(agentid,position):
     
    if not globalvars.database:
        return 0
    else:
        for key, value in globalvars.database.items():#my_id
            for ky, val in globalvars.database[key].items():#other_id
                if ky == agentid:
                    globalvars.database[key][ky]['position'] = position




def check_confdatabase(my_id,other_id,position,pos_time):
    

    print("AGENT ",my_id,": Retrieving confidence for position ",position,"at time",pos_time,"for agent",other_id)
    print(globalvars.database)

    if not globalvars.database:
        return 0
    else:
        for key, value in globalvars.database.items():#my_id
            if key == my_id:
                for ky, val in globalvars.database[key].items():#other_id
                    if ky == other_id:
                        for ky, val in globalvars.database[key].items():#other_id
                           # if globalvars.database[key][ky]['position'] == position:
                            if globalvars.database[key][ky]['position'] == position and globalvars.database[key][ky]['time_of_position'] <= pos_time:
                                #if same position at a different time, then update the time because the agent is not moving
                                return globalvars.database[key][ky]['confidence']
                                
    print("returning default")
    return 0




def check_assertiondatabase(my_id,other_agent,assertion_pos,pos_time):


    #check assertion database
    print("AGENT ",my_id,": Checking assertion database for position ",assertion_pos,"at time",pos_time,"for agent",other_agent)
    print(globalvars.assertion)
    if not globalvars.assertion:
        print("No agent made that assertion before")
        return 999
    else:
        for i in range(len(globalvars.assertion)):
            if globalvars.assertion[i]['my_id'] == my_id and globalvars.assertion[i]['other_id'] == other_agent and globalvars.assertion[i]['position'] == assertion_pos and globalvars.assertion[i]['sender'] != other_agent:
            #if globalvars.assertion[i]['my_id'] == my_id and globalvars.assertion[i]['other_id'] == other_agent and globalvars.assertion[i]['position'] == assertion_pos and globalvars.assertion[i]['time_of_position'] == pos_time:
                return globalvars.assertion[i]['sender']

    print("Debug: No agent made that assertion before")
    return 999


def print_database(event_time):
     
    #decay of ALL the confidence values
    if not globalvars.database:
        print("SIMULATOR: Nothing to read in database at ",event_time)
    if globalvars.database:
        print("SIMULATOR: Updating database at ",event_time)
        for key, value in globalvars.database.items():
            for ky, val in globalvars.database[key].items():
               for k, v in globalvars.database[key][ky].items():
                    if k == 'confidence':
                        globalvars.database[key][ky]['confidence'] = globalvars.database[key][ky]['confidence']-globalvars.delta*(event_time-globalvars.database[key][ky]['update_time'])
                        if globalvars.database[key][ky]['confidence'] < 0:
                            globalvars.database[key][ky]['confidence'] = 0
                        globalvars.database[key][ky]['update_time'] = event_time
                    else:
                        continue

    for key, value in globalvars.database.items():
        if key == 0:
            for ky, val in globalvars.database[key].items():
                if ky == 1:
                    row = [ky, globalvars.database[key][ky]['position'],globalvars.database[key][ky]['confidence'],globalvars.database[key][ky]['update_time']]
                    with open("conf.csv", 'a') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(row)

        #save to print to excel sheet for 3 agents
        for key, value in globalvars.database.items():
            for ky, val in globalvars.database[key].items():
               for k, v in globalvars.database[key][ky].items():
                   if key == 0 and ky == 1:
                       globalvars.arr01.append(globalvars.database[key][ky]['confidence'])
                       globalvars.time01.append(globalvars.database[key][ky]['update_time'])
                   if key == 0 and ky == 2:
                       globalvars.arr02.append(globalvars.database[key][ky]['confidence'])
                       globalvars.time02.append(globalvars.database[key][ky]['update_time'])
                   if key == 1 and ky == 2:
                       globalvars.arr12.append(globalvars.database[key][ky]['confidence'])
                       globalvars.time12.append(globalvars.database[key][ky]['update_time'])
                   if key == 1 and ky == 0:
                       globalvars.arr10.append(globalvars.database[key][ky]['confidence'])
                       globalvars.time10.append(globalvars.database[key][ky]['update_time'])
                   if key == 2 and ky == 1:
                       globalvars.arr21.append(globalvars.database[key][ky]['confidence'])
                       globalvars.time21.append(globalvars.database[key][ky]['update_time'])
                   if key == 2 and ky == 0:
                       globalvars.arr20.append(globalvars.database[key][ky]['confidence'])
                       globalvars.time20.append(globalvars.database[key][ky]['update_time'])


    contents = "%s at time %f\n" % (globalvars.database, event_time)
    dbfile = "database_%d.txt" % (globalvars.testcase)
    write_to_file(dbfile,contents)

   # string =""
   # dbfile1 = "database_for_plot_%d.txt" % (globalvars.testcase)
   # 
   # for key, value in globalvars.database.items():
   #     for ky, val in globalvars.database[key].items():
   #        dbfile1 = "database_for_plot_%d_%d.txt" % (key,ky)
   #        string += str(globalvars.database[key][ky]['position'])
   #        string += " "
   #        string += str(globalvars.database[key][ky]['confidence'])
   #        string += " "
   #        string += str(globalvars.database[key][ky]['update_time'])
   #        string += '\n'
   #        write_to_file(dbfile1,string)


def print_to_excel():
    import pandas as pd
    
    array = [globalvars.time01,globalvars.arr01,globalvars.time02,globalvars.arr02,globalvars.time10,globalvars.arr10,globalvars.time12,globalvars.arr12,globalvars.time21,globalvars.arr21,globalvars.time20,globalvars.arr20]

    df = pd.DataFrame(array).T

    filepath = "./confidence_plots-%d.xlsx" % (globalvars.testcase)
    df.to_excel(excel_writer = filepath,index=False,header=False)
    #df.to_excel(excel_writer = "./confidence_plots.xlsx")



def update_confidence(direct_verification,my_id,e,timeofevent):

    broadcast = 0

    if direct_verification:
        agent = my_id
        success = is_success_response(e['details']['prover'])

        prover = e['details']['prover'] #agent whose position has to be proved correct
        claimant = e['details']['claimant']

        print("SIMULATOR:prover:",prover,"claimant=",claimant)
        if success == 1:#direct verification success
            confidence = globalvars.direct_verification_score
            update_assertiondatabase(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)


            #time of position is from response == assertion
            update_confdatabase(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
            print("AGENT ",agent,": Updating confidence about position of agent ",prover," based on direct verification.")
            print("AGENT ",agent,": Confidence about position of agent ",prover,"=",confidence)
            print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])


            broadcast = 1 #How many times the same direct verification is to be sent
    


        if success == 0:#direct verification failure
            confidence = 0 #TODO should reduce by a factor V(d)
            #update_assertiondatabase(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
            update_confdatabase(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
            print("AGENT ",agent,": Updating confidence about position of agent ",prover," based on direct verification.")
            print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])




    return broadcast,confidence


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
   

def create_response(prover,challenger,claimant,timeofpos,pos,resp):
    response = {'prover':"DEFAULT", 'challenger':"DEFAULT",'claimant':"DEFAULT",'prover_pos_time':0,'position':(0,0,0),'response':"yes"}

    response['prover'] = prover
    response['challenger'] = challenger
    response['claimant'] = claimant
    response['prover_pos_time'] = timeofpos
    response['position'] = pos
    response['response'] = resp

    return response


def respond_to_challenge(tau):
    '''agent is turning flashlight on and off'''

    #incrementing the current time by the time it should take to perform the challenge-reponse
    #to indicate a successful response

    return 1


def is_success_response(agent):
        return 1



def calc_distance(i,j):

    import math
    import numpy as np

    '''calculating distance between  agent i and j'''

    p = np.array([globalvars.pos[i][0],globalvars.pos[i][1],globalvars.pos[i][2]])
    q = np.array([globalvars.pos[j][0],globalvars.pos[j][1],globalvars.pos[j][2]])
    d = np.linalg.norm(p-q) 

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


def create_event(eventid,nodeid,packetdetails,timeofevent):
    event = {'event_id':"DEFAULT", 'agent':0,'time':0}
    event['event_id'] = eventid
    event['agent'] = nodeid #agent creating the event
    event['time'] = timeofevent
    event['details'] = packetdetails
    
    return event


def process_event(e):
    
    #Everytime an event is processed, print the database
    if "DATABASE" in e['event_id']:
        
        ret = 1
        if ret:
            #generate another database update
           #set granularity
            timeofevent = e['time']
            #Trigger database refresh for all agents
            #for i in range(globalvars.number_of_nodes):
            node_handler(0,"UPDATE_DATABASE",e,timeofevent)



    if "ASSERTION" in e['event_id']:

                #if positions  have changed, the event position needs an update
        if globalvars.change_position:
            e['details']['position'] = globalvars.pos[e['details']['agent']]
            update_position_in_database(e['details']['agent'],e['details']['position'])
        

        #send challenge for each position claim from each agent that received the claim

        for i in range(globalvars.number_of_nodes): #everyone received because wireless communication is infinite
            if e['agent'] != i:#e['agent'] is making the assertion; does not need to receive it
                if e['details']['agent'] != i:#e['details']['agent'] is the agent whose position is in the assertion, so does not need to verify

                    ret = check_verifiability(e['details']['agent'],i)#e['details']['agent'] is the agent about whom te assertion is made 
                    dist = calc_distance(e['details']['agent'],i)
                    transmission_delay = 0.008 #seconds
                    dist = 0.3048*100*dist
                    propagation_delay = dist/globalvars.speed
                    timeofevent = e['time'] + transmission_delay + propagation_delay
                    #at timeofevent challenge will be received at agent i

                    if ret > 0:
                        #it is verifiable, i.e. direct verification is possible
                        print("AGENT ",i,": Can directly verify the position of agent ",e['details']['agent'])
                       
                        #since direct verification is possible, check if previously I have verified

                        #check confidence-database directly to find what the previous confidence is if already received an assertion for the same position (does not matter from where the previous assertion was from)  
                        confidence = check_confdatabase(i,e['details']['agent'],e['details']['position'],e['details']['timeofposition']) 
                        
                        print("DEBUG: Current Confidence:",confidence)
                        #if challenge not done yet or if the confidence is less than cf_min (Confidence Threshold)
                        if confidence < globalvars.cf_min:
                            node_handler(i,"SEND_AND_RECEIVE_CHALLENGE",e,timeofevent)


                    

    if "CHALLENGE" in e['event_id']:

        print("SIMULATOR: Event:",e)
        timeofevent = e['time']+ e['details']['tau']  
        for i in range(globalvars.number_of_nodes):
            if e['details']['prover'] == i:
                node_handler(i,"RESPOND_TO_CHALLENGE",e,timeofevent)
                
                
    if "RESPONSE" in e['event_id']:
        
        print("SIMULATOR: Event:",e)
        timeofevent = e['time']+globalvars.e_now #time of response = time of confidence update = time of response + e_now (a smal time period after the response accounted for update time) 
        node_handler(e['details']['challenger'],"CONFIDENCE_UPDATE_DIRECT_VERIF",e,timeofevent)
    


def node_handler(node_id,action,e,timeofevent):
    
    if action == "UPDATE_DATABASE":
        print_database(timeofevent)
        event_id = "DATABASE_%03d" % (globalvars.idn)
        globalvars.idn += 1
        update = "DB is updated"
        
        timeofevent = timeofevent+1

        #if globalvars.now < 600:
        if globalvars.now < 300:
            print("SIMULATOR: Adding event for reading database at ",timeofevent)
            e = create_event(event_id,node_id,update,timeofevent)
            globalvars.event_queue.append(deepcopy(e))

            #sort queue according to the simulated real time (time of event happening)
            globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])


    if action == "SEND_PERIODIC_ASSERTION":

        #node_id is sending position claim
        assertion = update_assertion(node_id,node_id,globalvars.pos[node_id],globalvars.direct_verification_score,timeofevent,timeofevent)

        event_id = "ASSERTION_%03d" % (globalvars.idn)
        globalvars.idn += 1

        print("SIMULATOR: Adding event for agent ",node_id," sending periodic assertion at ",timeofevent)
        print("SIMULATOR: Position for agent ",node_id," in periodic assertion at ",timeofevent, " is ",globalvars.pos[node_id])
        e = create_event(event_id,node_id,assertion,timeofevent)
        globalvars.event_queue.append(deepcopy(e))

        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])
        



    if action == "SEND_AND_RECEIVE_CHALLENGE":
        #node_id is sending challenge
            
        #e is for assertion event; using this e a new event will be created
        #challenger is the agent that received the assertion
        challenge = create_challenge(e['details']['sender'],e['details']['agent'],node_id,e['details']['position'],e['details']['timeofposition']) #sender of assertion
        

        event_id = "CHALLENGE_%03d" % (globalvars.idn)

        timeofpos = e['details']['timeofposition']
        globalvars.idn += 1

        # creating event e for sending challenge event 
        print("SIMULATOR: Adding event for agent ",node_id," sending challenge at ",timeofevent)
        e = create_event(event_id,node_id,challenge,timeofevent)# this is the time challenge was received by the receiver agent
        globalvars.event_queue.append(deepcopy(e))

        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

        
        
    if action == "RESPOND_TO_CHALLENGE":
        #node_id will respond to challenge by turning on/off flashlight
        ret = respond_to_challenge(e['details']['tau'])

        if ret == 1:
            response = create_response(e['details']['prover'],e['details']['challenger'],e['details']['claimant'],e['details']['time_of_position'],e['details']['position'],"yes")
        
        event_id = "RESPONSE_%03d" % (globalvars.idn)
        globalvars.idn += 1
        #node_id is responding to challenge
        print("SIMULATOR: Adding event for agent ",node_id," responding to a challenge at ",timeofevent)
        e = create_event(event_id,node_id,response,timeofevent)#timeofevent is the time at which agent will have successfully performed the challenge
        globalvars.event_queue.append(deepcopy(e))
        
        #sort queue according to the simulated real time (time of event happening)
        globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

        
    if action == "CONFIDENCE_UPDATE_DIRECT_VERIF":

        if "RESPONSE" in e['event_id']:
        #if challenge-response happened, node_id verifies response, then increases/decreases confidence

            print("AGENT ",node_id,": Updating confidence about position of agent",e['details']['prover'],"at ",timeofevent)
            ret,conf = update_confidence(1,node_id,e,timeofevent)


            if ret:
                #broadcast assertion with updated confidence

                #if position has changed then update in simulator's database
                if globalvars.pos[e['details']['prover']] != e['details']['position']:
                    globalvars.pos[e['details']['prover']] = e['details']['position']
                
                #node_id is sending position claim
                assertion = update_assertion(node_id,e['details']['prover'],e['details']['position'],conf,e['details']['prover_pos_time'],timeofevent)

                event_id = "ASSERTION_%03d" % (globalvars.idn)
                globalvars.idn += 1

                print("SIMULATOR: Adding event for agent ",node_id," sending assertion about position of agent ",e['details']['prover'],"at ",timeofevent)
                e = create_event(event_id,node_id,assertion,timeofevent)
                globalvars.event_queue.append(deepcopy(e))

                print("assertion:",e)

                #sort queue according to the simulated real time (time of event happening)
                globalvars.event_queue = sorted(globalvars.event_queue, key=lambda x: x['time'])

    

def change_position():
        #change agent positions
        filename = "pos_change_%d.txt" % (globalvars.testcase)
        globalvars.pos = eval(read_file(filename))
        print("SIMULATOR: position of all agents: ",globalvars.pos)

    

def main():
    '''Simulation engine'''
    
    #cparse argumentd
    if len(sys.argv) < 3:
        print("Usage: simulator_engine.py <number of nodes> <testcase number>")
        sys.exit();
    
    globalvars.init()
    globalvars.number_of_nodes = int(sys.argv[1])
    globalvars.testcase = int(sys.argv[2])

    print("SIMULATOR: Number of agents = ", globalvars.number_of_nodes)

    #create agent positions
    filename = "pos_%d.txt" % (globalvars.testcase)
    globalvars.pos = eval(read_file(filename))
    print("SIMULATOR: position of all agents: ",globalvars.pos)
   

    #add first event(s) to the event_queue
    e = {'event_id':"DEFAULT", 'agent':0,'time':0}


    
    ctr = 0
    #while ctr < 1:
    while ctr < 20:
        for i in range(globalvars.number_of_nodes):
            node_handler(i,"SEND_PERIODIC_ASSERTION",e,ctr*globalvars.refresh_period)
        ctr = ctr + 1
    node_handler(0,"UPDATE_DATABASE",e,0);

    fields = ['other_id','position','confidence','time']
    with open("conf.csv", 'w') as csvfile:  
    # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
        csvwriter.writerow(fields)

        
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
        globalvars.now = item['time']

        if globalvars.now >= 200:
            if globalvars.testcase == 7:
            #For agent motion
                change_position()
                globalvars.change_position = 1

              #  x = threading.Thread(target=change_position,daemon=True)
              #  x.start()

        
        #process the events till 2 refresh periods
       # if globalvars.now >= 130:
        #    break

    

    print_to_excel()

    print("SIMULATOR: End: assertion database",globalvars.assertion)
    


if __name__=="__main__":
    main()
