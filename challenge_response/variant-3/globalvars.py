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
    global trust_table
    global speed
    global database
    global assertion
    global flag
    global delta
    global refresh_period
    global direct_verification_score
    global cf_min
    global change_position
    global testcase
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
    global trust02  #0 database for 2
    global trust20 #0 database for 2
    global trust01  #0 database for 2
    global trust12  #0 database for 2
    global trust21 #0 database for 2
    global trust10 #0 database for 2
    global print_trust
    

    number_of_nodes = 0
    pos = []
    topology = 0
    event_queue = []
    now = 0
    idn = 0
    e_now = 0.2
    trust_table = defaultdict(dict)
    speed = 299792458 #m / s
    database = defaultdict(dict)
    assertion = []
    flag = 0
    #temporarily disable
    #delta = 0
    #reduce by 1 in 1 second
    delta = 1
    #delta = 0.1
    refresh_period = 15
    direct_verification_score = 20
    cf_min = 5
    change_position = 0
    testcase = 1
    print_trust = 0
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
    trust02 = ['trust02'] #0 database for 2
    trust20 = ['trust20'] #0 database for 2
    trust01 = ['trust01'] #0 database for 2
    trust12 = ['trust12'] #0 database for 2
    trust21 = ['trust21']#0 database for 2
    trust10 = ['trust10']#0 database for 2


