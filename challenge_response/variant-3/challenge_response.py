import globalvars
import numpy as np
import random

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

def update_confidence(direct_verification,agent,e,timeofevent):

    broadcast = 0

    if direct_verification:
        success = is_success_response(e['details']['prover'])

        prover = e['details']['prover'] #agent whose position has to be proved correct
        claimant = e['details']['claimant']
        if success == 1:#direct verification success
            confidence = globalvars.direct_verification_score
            update_database(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
            print("AGENT ",agent,": Updating confidence in position of agent ",prover," based on direct verification.")
            print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])


            broadcast = 1

            #update trust
            if globalvars.trust_table[agent][prover] == 0:
                globalvars.trust_table[agent][prover] = confidence
            else:
                globalvars.trust_table[agent][prover] = globalvars.trust_table[agent][prover]*confidence
                globalvars.trust_table[agent][prover] = (globalvars.trust_table[agent][prover]-0)/(globalvars.direct_verification_score-0)


        if success == 0:#direct verification failure
            confidence = 0 #TODO should reduce by a factor V(d)
            update_database(agent,prover,claimant,e['details']['position'],e['details']['prover_pos_time'],confidence,timeofevent)
            print("AGENT ",agent,": Updating confidence in position of agent ",prover," based on direct verification.")
            print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])

    if not direct_verification:

        claimant = e['details']['sender']
        prover = e['details']['agent'] #agent whose position has to be proved correct
        trust = globalvars.trust_table[agent][claimant]
        confidence = e['details']['confidence']*trust 
        update_database(agent,prover,claimant,e['details']['position'],e['details']['timeofposition'],confidence,timeofevent)
        print("AGENT ",agent,": Updating confidence in position of agent ",prover," based on trust.")
        print("SIMULATOR: Database at time ",timeofevent,"for agent",agent,":", globalvars.database[agent])

        broadcast = 1

    


    return broadcast,confidence


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
