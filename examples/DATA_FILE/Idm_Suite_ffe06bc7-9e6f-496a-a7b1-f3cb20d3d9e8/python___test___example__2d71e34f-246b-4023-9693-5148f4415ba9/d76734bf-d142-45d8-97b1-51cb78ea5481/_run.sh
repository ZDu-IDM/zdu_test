#!/bin/bash

# define the handler function
term_handler()
{
    # do whatever cleanup you want here
    echo "-1" > job_status.txt
    exit -1
}

# Register cleanup function to handle SIGINT and SIGTERM signals
trap 'term_handler' SIGINT SIGTERM

n=0


until [ "$n" -ge 1 ]
do
    echo "100" > job_status.txt
    
        exec -a "SIMULATION:d76734bf-d142-45d8-97b1-51cb78ea5481"  python3 Assets/simple.py --config config.json &
    

   child_pid=$!
   echo "Running simulation with PID: $child_pid"
   # Wait for the child process to complete
   wait $child_pid

   RESULT=$?
   if [ $RESULT -eq 0 ]; then
      echo "0" > job_status.txt
      exit $RESULT
   fi
   n=$((n+1))
done
echo "-1" > job_status.txt
exit $RESULT