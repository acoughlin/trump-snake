# alexander coughlin

from graphics import *
import time
import random
import collections

segment_list = collections.OrderedDict()
segment_box_list = collections.OrderedDict()
turn_list = collections.OrderedDict()
powerup_list = collections.OrderedDict()

win = GraphWin("Comp151", 800, 600)
dx = 1
dy = 1
respawn_timer_seconds = 4
refresh_timer_seconds = .005
first_four_segment_count = 1
total_time_in_hundredths_of_second = 0
new_segment_time_index = 0
first_point = Point(375, -25)
last_segment_time = 0

trump_image = Image((first_point), "trump.png")
segment_list[trump_image] = "Down"
trump_image.draw(win)

pointlistX = []
pointlistY = []
jeblist = []

def pointGenerator():
    for n in range(775):
        if((n % 25 == 0) & (n % 2 == 1)):
            if(n==375):
                continue
            pointlistX.append(n)
    for n in range(575):
        if((n % 25 == 0) & (n % 2 == 1)):
            pointlistY.append(n)


def jebGenerator():
    for n in range(4):
        pointGenerator()
        new_point = Point(random.choice(pointlistX), random.choice(pointlistY))
        jeb_image = Image(new_point, "jeb.png")
        jeblist.append(jeb_image)
        jeb_image.draw(win)

def collision(collision_target_list):
    head = next(iter(segment_list))

    if(((head.getAnchor().getX() < 25) | (head.getAnchor().getX() > 775) |
           (head.getAnchor().getY() < 25) | (head.getAnchor().getY() > 575))):
        if(first_four_segment_count  > 3):
            return True
    head_right = head.getAnchor().getX() + head.getWidth() / 2
    head_left = head.getAnchor().getX() - head.getWidth() / 2
    head_top = head.getAnchor().getY() - head.getHeight() / 2
    head_bottom = head.getAnchor().getY() + head.getHeight() / 2

    segment_index = 0
    for target in collision_target_list:
        if(target != head):
            voverlap = True
            hoverlap = True
            target_right = target.getAnchor().getX() + target.getWidth() / 2
            target_left = target.getAnchor().getX() - target.getWidth() / 2
            target_top = target.getAnchor().getY() - target.getHeight() / 2
            target_bottom = target.getAnchor().getY() + target.getHeight() / 2

            if((head_left + 30 > target_right) | (head_right - 30 < target_left)):
                hoverlap = False
            if((head_top + 30 > target_bottom) | (head_bottom - 30 < target_top)):
                voverlap = False
            if((voverlap == True) & (hoverlap == True)):
                # Safely handle deletion of overlapping segment, whether segment(dict) or powerup(list)
                if(isinstance(collision_target_list, collections.OrderedDict)):
                    del collision_target_list[target]
                else:
                    collision_target_list.remove(target)
                target.undraw()
                return True;
        segment_index =  segment_index + 1

def turnChecker(segment):
    if ((segment.getAnchor().getY() % 25 == 0) & (segment.getAnchor().getX() % 25 == 0)):
        for turn_point in turn_list:
            segX = segment.getAnchor().getX()
            segY = segment.getAnchor().getY()
            turnX = turn_point.getX()
            turnY = turn_point.getY()
            if (segX == turnX) & (segY == turnY):
                segment_list[segment] = turn_list[turn_point]
                if (segment == list(segment_list.keys())[-1]):
                    del turn_list[turn_point]


def main():
    global first_four_segment_count
    global new_segment_time_index
    global last_segment_time
    global total_time_in_hundredths_of_second
    jebGenerator()
    while (True):
        for segment in segment_list:
             # checks to see if it has to turn, changes direction if so.
            turnChecker(segment)

            if segment_list[segment] == "Down":
                segment.move(0, dy)
            elif segment_list[segment] == "Up":
                segment.move(0, -dy)
            elif segment_list[segment] == "Left":
                segment.move(-dx, 0)
            else:  # Right
                segment.move(dx, 0)

            # Makes the first 4 segments
            if ((segment == list(segment_list.keys())[-1]) & (segment.getAnchor().getY() + first_point.getY() == 5) & (
                len(segment_list) < 4) & (first_four_segment_count < 4)):
                trump_image = Image((first_point), "trump.png")
                segment_list[trump_image] = "Down"
                trump_image.draw(win)
                first_four_segment_count = first_four_segment_count + 1
                if(first_four_segment_count == 4):
                    last_segment_time = time.monotonic()

        # If key is pressed, add the turn-point to the list of turn-points
        movement = win.checkKey()
        if movement:
            if(movement == "space"):
                print("pause")
            # segment_list[next(iter(segment_list))] = movement
            current_direction = segment_list[next(iter(segment_list))]
            head = next(iter(segment_list))
            if ((current_direction == "Down") & ((movement == "Right") | (movement == "Left"))):
                x = head.getAnchor().getX()
                rounded = (head.getAnchor().getY() + 50) // 25
                if (rounded % 2 == 0):
                    rounded = rounded - 1
                y = rounded * 25
                turn_point = Point(x, y)
                turn_list[turn_point] = str(movement)
            elif ((current_direction == "Up") & ((movement == "Right") | (movement == "Left"))):
                x = head.getAnchor().getX()
                rounded = (head.getAnchor().getY()) // 25
                if (rounded % 2 == 0):
                    rounded = rounded - 1
                y = rounded * 25
                turn_point = Point(x, y)
                turn_list[turn_point] = str(movement)
            elif ((current_direction == "Left") & ((movement == "Up") | (movement == "Down"))):
                y = head.getAnchor().getY()
                rounded = (head.getAnchor().getX()) // 25
                if (rounded % 2 == 0):
                    rounded = rounded - 1
                x = rounded * 25
                turn_point = Point(x, y)
                turn_list[turn_point] = str(movement)
            elif ((current_direction == "Right") & ((movement == "Up") | (movement == "Down"))):
                y = head.getAnchor().getY()
                rounded = (head.getAnchor().getX() + 50) // 25
                if (rounded % 2 == 0):
                    rounded = rounded - 1
                x = rounded * 25
                turn_point = Point(x, y)
                turn_list[turn_point] = str(movement)

        if(collision(segment_list)):
            exit()

        # Makes new segments every every 4 seconds
        if((last_segment_time != 0) & (time.monotonic() - last_segment_time > respawn_timer_seconds)):
            if(segment_list[list(segment_list.keys())[-1]] == "Down"):
                new_point = Point(list(segment_list.keys())[-1].getAnchor().getX(), list(segment_list.keys())[-1].getAnchor().getY()-50)
            elif(segment_list[list(segment_list.keys())[-1]] == "Up"):
                new_point = Point(list(segment_list.keys())[-1].getAnchor().getX(), list(segment_list.keys())[-1].getAnchor().getY()+50)
            elif(segment_list[list(segment_list.keys())[-1]] == "Left"):
                new_point = Point(list(segment_list.keys())[-1].getAnchor().getX()+50, list(segment_list.keys())[-1].getAnchor().getY())
            else:
                new_point = Point(list(segment_list.keys())[-1].getAnchor().getX()-50, list(segment_list.keys())[-1].getAnchor().getY())
            trump_image = Image(new_point, "trump.png")
            segment_list[trump_image] = segment_list[list(segment_list.keys())[-1]]
            trump_image.draw(win)
            last_segment_time = time.monotonic()

        if(collision(jeblist)):
            delete_number = len(segment_list)//2
            for n in range(delete_number):
                list(segment_list.keys())[-1].undraw()
                del segment_list[list(segment_list.keys())[-1]]


        time.sleep(refresh_timer_seconds)
        total_time_in_hundredths_of_second = total_time_in_hundredths_of_second + refresh_timer_seconds
        if(total_time_in_hundredths_of_second > 60):
            exit()
        new_segment_time_index = new_segment_time_index + refresh_timer_seconds

main()