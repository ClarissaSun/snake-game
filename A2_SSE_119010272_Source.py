import turtle
import random
import time

g_screen = None                           # Screen object
g_head = None                             # Head: will be a turtle object later
g_xhead = 0                               # The x and y coordinates of the head
g_yhead = 0                             
g_tails = []                              # A list to store all tails(turtle objects) that are already on the body
g_num_of_waiting_tails = 5                # The number of tails that still not being appended to the body be will be appended later
g_monster = None                          # Monster: will be a turtle object later
g_instruction = None                      # Instruction: will be a turtle object later
g_food_list = []                          # A list to store all foods(turtle objects)
g_num_of_food = 0                         # A number to show the food number that the snake collides
g_direction = None                        # The heading direction of the head
g_start_time = 0                          # The start time of the game
g_current_time = 0                        # The current time of the game
g_collision_times = 0                     # The times that monster-tail collision occurs
g_rate_of_monster = 0                     # The monster's moving rate
g_the_last_direction = None
g_mon_start_xcor = 0
g_mon_start_ycor = 0


# Set up Screen
def configure_screen():
    global g_screen
    g_screen = turtle.Screen()
    g_screen.title(" Clarissa's snake game")
    g_screen.bgcolor("white")
    g_screen.setup(width=500,height=500)
    g_screen.tracer(0)
    return g_screen

# Create a turtle
def configure_turtle(shape="square", fillcolor="red", pencolor="red", x=0, y=0):
    tt = turtle.Turtle()
    tt.shape(shape)
    tt.fillcolor(fillcolor)
    tt.pencolor(pencolor)
    tt.penup()
    tt.goto(x, y)
    return tt

# Show the instruction
def instruction():
    global g_instruction
    g_instruction = turtle.Turtle()
    g_instruction.hideturtle()
    g_instruction.penup()
    g_instruction.goto(-10,30)
    g_instruction.write('''Welcome to Clarissa's version of snake!\n
You are going to use the 4 arrow keys to move the snake around the screen.\n 
Use space bar to pause and unpause during the game.\n
Try to consume all food items before the monster catches you.\n
Are you ready?\n
Let's begin! Click your mouse to start! ''',
    align="center", font=('Times New Roman', 10, "normal"))

def monster_start_point():
    global g_mon_start_xcor
    global g_mon_start_ycor
    while True:
        g_mon_start_xcor = random.randint(-240,240)
        g_mon_start_ycor = random.randint(-240,240)
        if not (-120 < g_mon_start_xcor < 120 and -120 < g_mon_start_ycor < 120):
            break
        
# Create 9 foods and store them in the g_food_list
# The index of food = (the number that the food represents) - 1
def configure_food():
    global g_food_list
    xList = [i for i in range(-230,230)] 
    yList = [i for i in range(-230,230)]
    l_food_x = random.sample(xList, 9)
    l_food_y = random.sample(yList, 9)

    for i in range(9):
        food = configure_turtle(pencolor="black", x=l_food_x[i], y=l_food_y[i])
        food.hideturtle()
        food.write(str(i+1),font=('Times New Roman', 12, "normal"))
        g_food_list.append(food)
    g_screen.update()

# A configuration of keys
def configure_keys():
    global g_screen
    g_screen.onkey(down,"Down")
    g_screen.onkey(up,"Up")
    g_screen.onkey(left,"Left")
    g_screen.onkey(right,"Right")
    g_screen.onkey(pause_and_ctn,"space")


# Four moveUp/down/left/right functions are used to move the head by controlling the turtle: g_head
def moveUp(d=20):
    global g_xhead
    global g_yhead
    g_xhead = g_head.xcor()
    g_yhead = g_head.ycor()
    g_head.setheading(90)
    g_head.forward(d)

def moveDown(d=20):
    global g_xhead
    global g_yhead
    g_xhead = g_head.xcor()
    g_yhead = g_head.ycor()
    g_head.setheading(270)
    g_head.forward(d)

def moveLeft(d=20):
    global g_xhead
    global g_yhead
    g_xhead = g_head.xcor()
    g_yhead = g_head.ycor()
    g_head.setheading(180)
    g_head.forward(d)

def moveRight(d=20):
    global g_xhead
    global g_yhead
    g_xhead = g_head.xcor()
    g_yhead = g_head.ycor()
    g_head.setheading(0)
    g_head.forward(d)


# Four down/up/left/right keys are used to pass and save the given direction 
def down():
    global g_direction
    global g_the_last_direction
    g_direction = 'down'
    g_the_last_direction = 'down'

def up():
    global g_direction
    global g_the_last_direction
    g_direction = 'up'
    g_the_last_direction = 'up'

def left():
    global g_direction
    global g_the_last_direction
    g_direction = 'left'
    g_the_last_direction = 'left'

def right():
    global g_direction
    global g_the_last_direction
    g_direction = 'right'
    g_the_last_direction = 'right'

# Control the snake to pause or continue by setting the g_direction as "" or resetting it as the last direction before a pause
def pause_and_ctn():
    global g_direction
    if g_direction == "":
        g_direction = g_the_last_direction
    else:
        g_direction = ""


# Move the head with the given direction
def move_of_head(direction):
    if direction == 'up':
        moveUp()
    elif direction == 'down':
        moveDown()
    elif direction == 'left':
        moveLeft()
    elif direction == 'right':
        moveRight()

# Moving the tails with the head
def move_of_tails(direction):
    if direction != "":
        l_tail_pos = []
        # Save all tails' positions in the list before they move
        if len(g_tails) != 0:
            for i in range(len(g_tails)):
                tail_pos = g_tails[i].position()
                l_tail_pos.append(tail_pos)
            # Move each tail to the position of the tail before them (the first tail to the position of the head)
            g_tails[0].goto(g_xhead, g_yhead)
            for i in range(1,len(g_tails)):
                g_tails[i].setposition(l_tail_pos[i-1])

def move_of_monster(angle,d = 20):
    if angle == 0 or angle == 90 or angle == 180 or angle == 270:
        g_monster.setheading(angle)
        g_monster.forward(d)
    elif 45 <= angle < 90:
        g_monster.setheading(90)
        g_monster.forward(d)
    elif 0 < angle < 45:
        g_monster.setheading(0)
        g_monster.forward(d)
    elif 90 < angle < 135:
        g_monster.setheading(90)
        g_monster.forward(d)
    elif 135<= angle < 180:
        g_monster.setheading(180)
        g_monster.forward(d)
    elif 180 < angle < 225:
        g_monster.setheading(180)
        g_monster.forward(d)
    elif 225 <= angle < 270:
        g_monster.setheading(270)
        g_monster.forward(d)
    elif 270 < angle < 315:
        g_monster.setheading(270)
        g_monster.forward(d)
    elif 315 <= angle < 360:
        g_monster.setheading(360)
        g_monster.forward(d)
    g_screen.update()


# If the head collides with a food, retrieve the numer of the food, clear the food on the canvas, and subtitute it as 0 in the food list
def Food_Collision():
    global g_num_of_food
    global g_food_list
    for food in g_food_list:
        if food != 0 and g_head.distance(food) < 20:
            g_num_of_food = g_food_list.index(food) + 1
            print(g_num_of_food)
            food.clear()
            add_new_tails()
            g_food_list[g_food_list.index(food)] = 0

# Adding the number of waiting tails(tails that will be appended to the body later) according to the number of food retrieved
def add_new_tails():
    global g_num_of_waiting_tails
    g_num_of_waiting_tails += g_num_of_food

# If there is still tail to be appended, create a new turtle in list: g_tails, and -1 from the g_number_of_waiting_list
def append_a_tail_to_body():
    global g_tails
    global g_num_of_waiting_tails  
    if g_direction != "":
        if len(g_tails) != 0:
            tail = configure_turtle(fillcolor="black", pencolor = "red", x = g_tails[len(g_tails)-1].xcor(), y = g_tails[len(g_tails)-1].ycor())
        else:
            tail = configure_turtle(fillcolor="black", pencolor = "red", x = g_xhead, y = g_yhead)
        g_tails.append(tail)
        g_num_of_waiting_tails -= 1

# If the head collide with the border, set g_direction as "" to pause the snake
def BorderCollision():
    global g_direction
    if g_head.xcor() > 230 and g_direction == 'right':
        g_direction = ""
    elif g_head.xcor() < -230 and g_direction == 'left':
        g_direction = ""
    elif g_head.ycor() > 230 and g_direction == 'up':
        g_direction = ""
    elif g_head.ycor() < -230 and g_direction == 'down':
        g_direction = ""

# When a head-tail collision occurs, add 1 to the g_collision times
def count_tail_collisions():
    global g_collision_times
    for tail in g_tails:
        if g_monster.distance(tail) < 20:
            g_collision_times += 1


# Repeat the single motion of snake with consideration on other cases, like collides with a food/border/monster, etc.
def round_for_snake():
    if not done():
        configure_keys()
        g_screen.listen()
        BorderCollision()

        if g_num_of_waiting_tails != 0:
            append_a_tail_to_body()
            Food_Collision()
            move_of_head(g_direction)
            move_of_tails(g_direction)
            g_screen.update()
            if not done():
                g_screen.ontimer(round_for_snake,300)

        elif g_num_of_waiting_tails == 0:
            Food_Collision()
            move_of_head(g_direction)
            move_of_tails(g_direction)
            g_screen.update()
            if not done():
                g_screen.ontimer(round_for_snake,200)

# Repeat the single motion of monster with until it collides with the head. 
# Update the passed time and tail-monster collision time in every motion of the monster.
def round_for_monster():
    global g_rate_of_monster
    global g_collision_times
    global g_current_time
    global g_direction
    count_tail_collisions()
    g_current_time = time.time()
    g_screen.title("current time: "+str(int(g_current_time - g_start_time))+"   "+"collision:" + str(g_collision_times))
    g_screen.update()
    if not done():
        g_rate_of_monster = random.randint(-100,100)
        angle = g_monster.towards(g_head)
        move_of_monster(angle)
        g_screen.ontimer(round_for_monster, 300+g_rate_of_monster)

# Check if the game ends. 
def done():
    global g_food_list
    if g_monster.distance(g_head) <20:
    # If the monster collides with the head, the gamer loses
        done = configure_turtle()
        done.hideturtle()
        done.write("GameOver!",font=('Times New Roman', 15, "normal"))
        return True  
    else:
    # If the snake clears all food, the gamer wins
        a = len(set(g_food_list))
        if a == 1:
            done = configure_turtle()
            done.hideturtle()
            done.write("You win!",font=('Times New Roman', 15, "normal"))
            return True
        
def start(x,y):
    global g_instruction
    global g_direction
    global g_start_time
    global g_current_time
    global g_screen
    global g_the_last_direction

    g_start_time = time.time()
    g_instruction.clear()
    # Clear the instructions.
    configure_food()
    # Show food
    g_direction = 'up'
    g_the_last_direction = 'up'
    # Set the initial move to be up
    g_current_time = time.time()
    g_screen.title("current time: "+str(int(g_current_time - g_start_time))+"   "+"total collision:" + str(count_tail_collisions()))
    # Show time
    g_screen.update()
    g_screen.ontimer(round_for_snake,500)
    g_screen.ontimer(round_for_monster, 1000)
    # Start the movement of snake and monster at different time.

def main():
    # Set up screen, head monster, instruction before user’s click.
    global g_screen
    global g_monster
    global g_head

    g_screen = configure_screen()
    g_screen.tracer(0)
    g_screen.listen()
    instruction()
    monster_start_point()
    g_monster = configure_turtle(fillcolor = "purple", pencolor= "purple", x = g_mon_start_xcor , y = g_mon_start_ycor )
    g_head = configure_turtle() 
    g_screen.update() 
    g_screen.onscreenclick(start)

main()
g_screen.mainloop()