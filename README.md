# bwsi-racecar-2026

This simple gap follower algorithm won the Grand Prix and set a new Time Trial record of 59s.

## Logic

The base algorithm is just a regular gap follower: the largest continuous run of LIDAR samples with a distance above a certain threshold, or zero distance(indicating the distance exceeds the max LIDAR range) is the "gap", and we use a proportional controller to track the center of the gap. We used the speed controller from the EATS (Elastic Autonomous Tracking System). It scales the robot speed with the average of the furthest distance on the left and right side of the LIDAR. This combination reached the highest speed on the Speed Quest of 4.5 m/s.

For the Grand Prix, we made three major changes to the codebase:
- We added a minimum gap size, which prevented the car from following noise when no gap was available. 
- We adjusted the range of the LIDAR scan. Since the course ran clockwise, we made the range of the right side of the car (70deg) more than the left side of the car (60deg). We also increased the range of the EATS speed controller to 110 degrees on each side, which helped in sharp corners.
- The last modification was to bias the car to follow the rightmost gap if the gap size was at least 60% of the size of the largest gap. This helped the robot on the forks but was mainly for preventing the car from entering the doom spiral, where the correct gap on the right side was smaller than the doom spiral gap on the left side. This is likely what caused the car to escape the course on the final straight (shoutout Pablo for saving the run).
