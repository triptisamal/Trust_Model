#!/bin/sh


echo "Choose what test scenario"
echo "0. 2 agents V(d) > 0"
echo "1. 2 agents V(d) < 0"
echo "2. 3 agents in straight line, all V(d) > 0"
echo "3. 3 agents in straight line, one V(d) < 0, one V(d) > 0"
echo "4. 3 agents in at corner of a triangle, all V(d) > 0"
echo "5. 3 agents in at corner of a triangle, two V(d) > 0, one V(d) < 0"
echo "6. 3 agents in at corner of a triangle, one V(d) > 0, two V(d) < 0"
echo "7. 3 agents, 1 agent moving such that it can not be verified by another agent that was able to verify the agent at its previous location."
echo "8. 3 agents, 1 agent moving such that the moving agent can be verified by another agent that was able to verify the agent at its previous location and another agent can be verified by some agent that was not able to verify the agent previously"
echo "9. 2 agents, V(d) was 0, changes to > 0"
echo "12. Test 0-d: 2 agents with V(d) > 0, one agent moves and V(d) changes to < 0"
echo "13. All: from 0 to 8"
echo "14. 12 agents, all stationary"
echo "15. 12 agents, all stationary but different positions"
echo "16. 12 agents, all stationary but different positions"
echo "17. 12 agents, one moving"


read testnumber


if [ "$testnumber" -eq "0" ] || [ "$testnumber" -eq "1" ] || [ "$testnumber" -eq "9" ] || [ "$testnumber" -eq "12" ]
then
	python3 simulator_engine.py 2 $testnumber >out_$testnumber
fi


if [ "$testnumber" -eq "2" ] || [ "$testnumber" -eq "3" ] || [ "$testnumber" -eq "4" ] || [ "$testnumber" -eq "5" ] || [ "$testnumber" -eq "6" ] || [ "$testnumber" -eq "7" ] || [ "$testnumber" -eq "8" ]


then
	#python3 simulator_engine.py 3 $testnumber 
	python3 simulator_engine.py 3 $testnumber >out_$testnumber
fi

if [ "$testnumber" -eq "14" ] || [ "$testnumber" -eq "15" ] || [ "$testnumber" -eq "16" ]  
then
	python3 simulator_engine.py 16 $testnumber >out_$testnumber
fi

if [ "$testnumber" -eq "10" ]
then
	c=0
	while [ "$c" -le "8" ]
	do 
		if [ $c -eq "0" ] || [ "$c" -eq "1" ]
		then
			python3 simulator_engine.py 2 $c >out_$c
			c=$(( c+1 ))
		fi
		if [ $c -eq "2" ] || [ "$c" -eq "3" ] || [ $c -eq "4" ] || [ "$c" -eq "5" ] || [ $c -eq "6" ] || [ $c -eq "7" ] || [ $c -eq "8" ]
		then
			python3 simulator_engine.py 3 $c >out_$c
			c=$(( c+1 ))
		fi
	done
fi

