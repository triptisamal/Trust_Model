from collections import defaultdict


#function definition
def init():
    global number_of_nodes
    global pos
    global topology
    global event_queue
    global now
    global idn
    global e_now
    global confidence_table
    global trust_table
    global max_reached
    global speed
    global database
    global flag
    global delta
    global refresh_period
    global direct_verification_score
    global cf_min
    global alpha
    global arr01 #0 database for 1
    global arr12 #1 database for 2 
    global arr20 #2 database for 0
    global arr21 #2 database for 1
    global arr10 #1 database for 0
    global arr02 #0 database for 2
    global time01 #0 database for 1
    global time12 #1 database for 2 
    global time20 #2 database for 0
    global time21 #2 database for 1
    global time10 #1 database for 0
    global time02 #0 database for 2
    

    number_of_nodes = 0
    pos = []
    topology = 0
    event_queue = []
    now = 0
    idn = 0
    e_now = 0.2
    confidence_table = defaultdict(dict)
    trust_table = defaultdict(dict)
    max_reached = 0
    speed = 299792458 #m / s
    database = defaultdict(dict)
    flag = 0
    delta = 1
    refresh_period = 15
    direct_verification_score = 20
    cf_min = 5
    alpha = 1 #trust score
    arr01 = ['01'] #0 database for 1
    arr12 = ['12'] #1 database for 2 
    arr20 = ['20'] #2 database for 0
    arr21 = ['21'] #2 database for 1
    arr10 = ['10'] #1 database for 0
    arr02 = ['02'] #0 database for 2
    time01 = ['t01'] #0 database for 1
    time12 = ['t12'] #1 database for 2 
    time20 = ['t20'] #2 database for 0
    time21 = ['t21'] #2 database for 1
    time10 = ['t10'] #1 database for 0
    time02 = ['t02'] #0 database for 2


