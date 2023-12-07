#!/bin/sh


echo "Choose what test scenario"
echo "0. 2 agents V(d) > 0"
echo "1. 2 agents V(d) < 0"
echo "2. 3 agents in straight line, all V(d) > 0"
echo "3. 3 agents in straight line, one V(d) < 0, one V(d) > 0"
echo "4. 3 agents in at corner of a triangle, all V(d) > 0"
echo "5. 3 agents in at corner of a triangle, two V(d) > 0, one V(d) < 0"
echo "6. 3 agents in at corner of a triangle, one V(d) > 0, two V(d) < 0"
echo "7. 2 agents with V(d) > 0, one agent moves and V(d) changes to < 0"
echo "8. All"

read testnumber


if [ "$testnumber" -eq "0" ] || [ "$testnumber" -eq "1" ] || [ "$testnumber" -eq "7" ]
then
	python3 simulator_engine.py 2 $testnumber >out_$testnumber
fi


if [ "$testnumber" -eq "2" ] || [ "$testnumber" -eq "3" ] || [ "$testnumber" -eq "4" ] || [ "$testnumber" -eq "5" ] || [ "$testnumber" -eq "6" ]
then
	python3 simulator_engine.py 3 $testnumber >out_$testnumber
fi

if [ "$testnumber" -eq "8" ]
then
	c=0
	while [ "$c" -le "7" ]
	do 
		if [ $c -eq "0" ] || [ "$c" -eq "1" ] || [ "$c" -eq "7" ]
		then
			python3 simulator_engine.py 2 $c >out_$c
			c=$(( c+1 ))
		fi
		if [ $c -eq "2" ] || [ "$c" -eq "3" ] || [ $c -eq "4" ] || [ "$c" -eq "5" ] || [ $c -eq "6" ]
		then
			python3 simulator_engine.py 3 $c >out_$c
			c=$(( c+1 ))
		fi
	done
fi

