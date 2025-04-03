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
    
        exec -a "SIMULATION:9a0a2059-7144-4c35-8f74-7a4dad2e2537"  python3 Assets/simple.py --config config.json &
    

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