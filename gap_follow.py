```
"""
MIT BWSI Autonomous RACECAR 2026
MIT License

Written by Team 4/cc (Paul Sopin, Andrew Pan, Jason Ma, Jason Zeng)
"""

import racecar_core
import racecar_utils as rc_utils

rc = racecar_core.create_racecar()

OPEN_THRESHOLD = 300.0
MIN_GAP_WIDTH = 15
TIE_RATIO = 0.6
GAP_TURN_KP = 0.008

SPEED_KP = 0.0016
MIN_SPEED = 0.7
MAX_SPEED = 1.0

speed = 0.0
angle = 0.0

left_dist = 0.0
right_dist = 0.0

left_angle = 0.0
right_angle = 0.0

def start():
    rc.drive.set_max_speed(1.0)
    rc.drive.set_speed_angle(0, 0)
    rc.display.show_text("CHRIS")

def update():
    global speed, angle
    global left_dist, right_dist

    scan = rc.lidar.get_samples()
    if len(scan) != 0:
        runs, current_run = [], []
        for deg in range(-60, 71, 1):
            cur_scan = rc_utils.get_lidar_average_distance(scan, deg % 360, 0.5)
            if cur_scan > OPEN_THRESHOLD or cur_scan == 0:
                current_run.append(deg)
            else:
                if len(current_run) >= MIN_GAP_WIDTH:
                    runs.append(current_run)
                current_run = []
        if len(current_run) >= MIN_GAP_WIDTH:
            runs.append(current_run)

        if runs:
            widest = max(len(r) for r in runs)
            contenders = [r for r in runs if len(r) >= TIE_RATIO * widest]
            best_run = max(contenders, key=lambda r: sum(r) / len(r))
            target_angle = sum(best_run) / len(best_run)
        else:
            target_angle = 0.0

        left_dist = 0
        for deg in range (-100, 0, 1):
            cur_scan = rc_utils.get_lidar_average_distance(scan, deg % 360, 0.5)
            if cur_scan > left_dist:
                left_dist = cur_scan

        right_dist = 0
        for deg in range (0, 101, 1):
            cur_scan = rc_utils.get_lidar_average_distance(scan, deg % 360, 0.5)
            if cur_scan > right_dist:
                right_dist = cur_scan

        avg_dist = (left_dist + right_dist) / 2

        angle = GAP_TURN_KP * target_angle
        angle = rc_utils.clamp(angle, -1.0, 1.0)
        speed = SPEED_KP * avg_dist
    else:
        speed = MAX_SPEED

    speed = rc_utils.clamp(speed, MIN_SPEED, MAX_SPEED)
    rc.drive.set_speed_angle(speed, angle)

    print("Speed:", speed, "Angle:", angle)
    print("Left:", left_dist, "Right:", right_dist)

def update_slow():
    pass

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
```
