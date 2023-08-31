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

    number_of_nodes = 0
    pos = []
    topology = 0
    event_queue = []
    now = 0
    idn = 0
    e_now = 1
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

