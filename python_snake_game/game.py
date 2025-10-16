import turtle
import time
import random
# import winsound # NOTE: winsound is limited to Windows and has been removed for portability.

# --- Game Setup ---
delay = 0.1 # Game speed control

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Python Snake Game 🐍")
wn.bgcolor("dark green") # BACKGROUND CHANGED TO DARK GREEN
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off the screen updates for manual updates (smoother animation)

# Snake head
head = turtle.Turtle()
head.speed(0) # Animation speed (0 is fastest)
head.shape("circle")
head.color("lime green") # Bright color for the head
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = [] # List to hold the snake's body segments

# Pen for Scoreboard
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# --- Functions ---

# Removed play_sound function due to platform dependency (winsound is Windows-only).
# If you are on Windows, you can uncomment this function and the winsound import.
# For cross-platform sound, consider using the 'playsound' or 'pygame' library.

def go_up():
    """Sets the snake direction to 'up', preventing instant reversal."""
    if head.direction != "down":
        head.direction = "up"

def go_down():
    """Sets the snake direction to 'down', preventing instant reversal."""
    if head.direction != "up":
        head.direction = "down"

def go_left():
    """Sets the snake direction to 'left', preventing instant reversal."""
    if head.direction != "right":
        head.direction = "left"

def go_right():
    """Sets the snake direction to 'right', preventing instant reversal."""
    if head.direction != "left":
        head.direction = "right"

def move():
    """Moves the snake head one step (20 units) in the current direction."""
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
        
def reset_game():
    """Resets the snake, scores, and screen upon collision."""
    global score, delay, high_score
    
    # Pause for a moment to indicate Game Over
    time.sleep(1)
    
    # Move head to center and stop
    head.goto(0, 0)
    head.direction = "Stop"

    # Hide the body segments (move them off-screen)
    for segment in segments:
        segment.goto(1000, 1000)

    # Clear the segments list
    segments.clear()

    # Reset current score and delay
    score = 0
    delay = 0.1

    # Update the scoreboard
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), 
               align="center", font=("Courier", 24, "normal"))


# --- Keyboard Bindings ---
wn.listen()
# Use arrow keys for controls
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# --- Main Game Loop ---
while True:
    wn.update()

    # 1. Check for **Border Collision** (Game Over)
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        reset_game()

    # 2. Check for **Food Collision**
    if head.distance(food) < 20:
        # Move the food to a new random position
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)

        # Add a new segment to the snake body
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("green") # Body color
        new_segment.penup()
        segments.append(new_segment)

        # Removed call to play_sound() because winsound is not cross-platform.
        # If you are on Windows, you can re-enable the play_sound function and winsound import.

        # Increase the score and speed up the game
        score += 10
        if score > high_score:
            high_score = score
        
        # Shorten the delay to increase speed (gets harder)
        if delay > 0.05: # Prevents delay from going too low
             delay -= 0.001

        # Update the scoreboard
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), 
                   align="center", font=("Courier", 24, "normal"))

    # 3. **Move the body segments**
    # Move the tail segments first, starting from the last one (index len-1) down to the first segment (index 1)
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 (the one right behind the head) to the head's current position
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    # Move the head itself
    move()

    # 4. Check for **Self-Collision** (Head hits body segment - Game Over)
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    # Apply the delay for game speed
    time.sleep(delay)

# This line ensures the window stays open after the loop potentially exits (though in this case the while True loop keeps it running)
# wn.mainloop() 
