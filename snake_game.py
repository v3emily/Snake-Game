import turtle
from enum import Enum
import time
import random


#Setting up screen#
screen = turtle.Screen()
screen.setup(width=612, height=612)
screen.tracer(0)


#Creating leaderboard#
class Leaderboard:
   def __init__(self):
       self.tbl = []
       self.current_score = 0
       self.all_scores = []
       title = turtle.Turtle()
       title.penup()
       title.goto(-500, 250)
       title.write('Leaderboard', move=False, align="left", font=("Arial", 15, "normal"))
       title.hideturtle()
       for i in range(5):
           hi_score = turtle.Turtle()
           hi_score.penup()
           hi_score.goto(-500, 250 - ((i+1) * 50))
           hi_score.hideturtle()
           self.tbl.append(hi_score)
#Change leaderboard based on top 5 scores#
   def update(self):
       for j in self.tbl:
           j.clear()
       if len(self.all_scores) == 1:
           self.tbl[0].write(f"{self.all_scores[0]}", move=False, align="left", font=("Arial", 15, "normal"))
           self.tbl[0].hideturtle()
       else:
           order_desc = self.all_scores.sort(reverse = True)
           for i in range(min(5, len(self.all_scores))):
               self.tbl[i].write(f"{self.all_scores[i]}", move=False, align="left", font=("Arial", 15, "normal"))
               self.tbl[i].hideturtle()

#Creating current score counter#
class CurrentCount:
   def __init__(self):
       self.current = 0
       title = turtle.Turtle()
       title.penup()
       title.goto(500, 250)
       title.write('Current Score', move=False, align="left", font=("Arial", 15, "normal"))
       title.hideturtle()
       self.cscore = turtle.Turtle()
       self.cscore.penup()
       self.cscore.goto(500, 200)
       self.cscore.hideturtle()
       self.cscore.write(f"{self.current}", move=False, align="center", font=("Arial", 15, "normal"))

leaderboard = Leaderboard()
current = CurrentCount()


#Creating item#
class Item:
  def __init__(self):
      self.body = turtle.Turtle()
      self.body.color("#FDD838")
      self.body.penup()
      self.place_item()
      self.draw_item()
#Place item in random location#
  def place_item(self):
       self.body.goto(((random.randint(-8, 7)*25)),((random.randint(-8, 7)*25)))
  def draw_item(self):
      self.body.shape("square")


item = Item()


#Setting up board#
class Board:
   def __init__(self, num_cols=17, num_rows=17, cell_item=None, grid=None):
       assert num_cols is not None and num_rows is not None
       assert type(num_cols) == int and type(num_rows) == int
       assert num_cols >= 0 and num_rows >= 0
       self.num_rows = num_rows
       self.num_cols = num_cols
       self.cell_color = turtle.Turtle()
       self.cell_color.speed(0)
       self.cell_color.penup()
       self.game_over = False
       if grid:
           assert num_cols * num_rows == len(grid)
           self.grid = grid[:]
       else:
           self.grid = [cell_item for _ in range(num_cols * num_rows)]
#Drawing and creating checkerboard pattern#
   def board_setup(self):
       for i in range(self.num_rows):
           for j in range(self.num_cols):
               coords = i*self.num_cols+j
               if coords%2 == 0:
                   self.cell_color.fillcolor("#9FB0DC")
               else:
                   self.cell_color.fillcolor("#AD7CCC")
               self.cell_color.goto((j*25-(425/2)),(i*25-(425/2)))
               self.cell_color.pendown()
               self.cell_color.begin_fill()
               for l in range(4):
                   self.cell_color.forward(25)
                   self.cell_color.right(90)
               self.cell_color.end_fill()
               self.cell_color.penup()
               self.cell_color.hideturtle()
   #Creating snake#
   class Snake:
       def __init__(self):
           self.head = turtle.Turtle()
           self.head.shape("square")
           self.body = []
           self.head.color("#0E7B29")
           self.head.penup()
           self.head.goto((8*25-(425/2)+(25/2)),(8*25-(425/2)+(25/2)))
           self.size = 1
           self.body.append(self.head)
   #Control snake; moving, preventing moving in opposite directions(ex: up -> down)#
       def movement(self):
           self.prev = [self.body[0].pos()]
           for i in range(len(self.body)-1, 0, -1):
               self.body[i].goto(self.body[i-1].pos())
           self.body[0].forward(25)
       def change_up(self):
           if self.body[0].heading() != 270:
               self.body[0].setheading(90)
       def change_right(self):
           if self.body[0].heading() != 180:
               self.body[0].setheading(0)
       def change_down(self):
           if self.body[0].heading() != 90:
               self.body[0].setheading(270)
       def change_left(self):
           if self.body[0].heading() != 0:
               self.body[0].setheading(180)
       #Keybinding#
       def control(self):
           screen.listen()
           screen.onkey(self.change_up, "w")
           screen.onkey(self.change_right, "d")
           screen.onkey(self.change_down, "s")
           screen.onkey(self.change_left, "a")
   #Setting Bounds#
       def bounds_check(self):
           if self.head.xcor() < (-425/2):
               board.game_over = True
           elif self.head.xcor() > (425/2):
               board.game_over = True
           elif self.head.ycor() < (-425/2)-25:
               board.game_over = True
           elif self.head.ycor() > (425/2)-25:
               board.game_over = True
           else:
               board.game_over = False
   #Add new body part#
       def add_body(self):
           body_part = turtle.Turtle()
           body_part.shape("square")
           body_part.color("#0E7B29")
           body_part.penup()
           if len(self.body) > 1:
               body_part.goto(self.body[-1].pos())
           else:
               body_part.goto(self.body[0].pos())
           self.body.append(body_part)
   #Overlap check#
       def overlap(self):
           for i in self.body[1:]:
               if self.head.distance(i) < 5:
                   board.game_over = True
                   break
               else:
                   board.game_over = False


#Item collect#
def collect():
   if snake.head.distance(item.body)<15:
       item.place_item()
       item.body.clear()
       item.draw_item()
       snake.add_body()
       leaderboard.current_score += 1
       current.current += 1
       current.cscore.clear()
       current.cscore.write(f"{current.current}", move=False, align="center", font=("Arial", 15, "normal"))



#Display instructions#
def instructions():
   text = turtle.Turtle()
   text.penup()
   text.goto(0, 350)
   text.write('w = Up,   a = Left,   s = Down,   d = Right', move=False, align="center", font=("Arial", 15, "normal"))
   text2 = turtle.Turtle()
   text2.penup()
   text2.goto(0, 300)
   text2.write('r = Play again', move=False, align="center", font=("Arial", 15, "normal"))
   text3 = turtle.Turtle()
   text3.penup()
   text3.goto(0, 250)
   text3.write('Press d to start', move=False, align="center", font=("Arial", 15, "normal"))
   text.hideturtle()
   text2.hideturtle()
   text3.hideturtle()


#Setting up game over#
def game_over():
   if board.game_over == True:
       snake.head.write('GAME OVER!', move=False, align="center", font=("Arial", 25, "normal"))
       leaderboard.all_scores.append(leaderboard.current_score)
       leaderboard.update()
       screen.onkey(reset, "r")


board = Board()
board.board_setup()


snake = Board.Snake()


#Calls core game functions + check game over#
def move():
   snake.control()
   snake.movement()
   snake.bounds_check()
   if not board.game_over:
       snake.overlap()
       collect()
   game_over()
   screen.listen()
   screen.update()
   if not board.game_over:
       screen.ontimer(move, 200)
   else:
       return


#Restart game#
def reset():
   board.game_over = False
   board.cell_color.clear()
   board.board_setup()
   for i in snake.body:
       i.clear()
       i.goto(10000000, 1000000)
   snake.body = []
   snake.head.clear()
   snake.head.goto(8*25-(425/2)+(25/2), 8*25-(425/2)+(25/2))
   snake.head.setheading(0)
   snake.body.append(snake.head)
   snake.size = 1
   item.body.clear()
   item.place_item()
   item.draw_item()
   leaderboard.current_score = 0
   leaderboard.update()
   current.current = 0
   current.cscore.clear()
   current.cscore.write(f"{current.current}", move=False, align="center", font=("Arial", 15, "normal"))
   screen.listen()
   go()
   screen.update()


#Running game#
def start():
   screen.onkey(None, "d")
   move()
def go():
   screen.listen()
   instructions()
   screen.onkey(start, "d")

go()

screen.update()
turtle.done()