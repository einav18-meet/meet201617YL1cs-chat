#2016-2017 PERSONAL PROJECTS: TurtleChat!
#EinavCohen

#####################################################################################
#                                   IMPORTS                                         #
#####################################################################################
import turtle
from turtle_chat_client import Client 
from turtle_chat_widgets import Button,TextInput
from abc import ABCMeta,abstractmethod
#####################################################################################
#####################################################################################
class TextBox (TextInput):
    def draw_box(self):
        self.boxx= turtle.clone()
        self.boxx.penup()
        self.boxx.goto(self.pos)
        self.boxx.pendown()
        self.boxx.goto(self.pos[0]+self.width,self.pos[1])
        self.boxx.goto(self.pos[0]+self.width,self.pos[1]+self.height)
        self.boxx.goto(self.pos[0],self.pos[1]+self.height)
        self.boxx.goto(self.pos)

    def write_msg(self):
        self.writer.clear()
        self.writer.write(self.new_msg)
        
#####################################################################################
#                                   TextBox                                         #
#####################################################################################
#Make a class called TextBox, which will be a subclass of TextInput.
#Because TextInput is an abstract class, you must implement its abstract
#methods.  There are two:
#
#draw_box
#write_msg
#
#Hints:
#1. in draw_box, you will draw (or stamp) the space on which the user's input
#will appear.
#
#2. All TextInput objects have an internal turtle called writer (i.e. self will
#   have something called writer).  You can write new text with it using code like    
#
#   self.writer.write(a_string_variable)
#
#   and you can erase that text using
#
#   self.writer.clear()
#
#3. If you want to make a newline character (i.e. go to the next line), just add
#   \r to your string.  Test it out at the Python shell for practice
#####################################################################################
#####################################################################################

#####################################################################################
#                                  SendButton                                       #
#####################################################################################
#Make a class called SendButton, which will be a subclass of Button.
#Button is an abstract class with one abstract method: fun.
#fun gets called whenever the button is clicked.  It's jobs will be to
#
# 1. send a message to the other chat participant - to do this,
#    you will need to call the send method of your Client instance
# 2. update the messages that you see on the screen
#
#HINT: You may want to override the __init__ method so that it takes one additional
#      input: view.  This will be an instance of the View class you will make next
#      That class will have methods inside of it to help
#      you send messages and update message displays.
#####################################################################################
#####################################################################################

class SendButton(Button):
    def __init__(self,view,my_turtle=None,shape=None,pos=(0,0)):
        self.aview = view
        super(SendButton,self).__init__(my_turtle,shape,pos)
        

    def fun(self,x,y):
        print('hi')
        self.aview.send_msg()
        
    
##################################################################
#                             View                               #
##################################################################
#Make a new class called View.  It does not need to have a parent
#class mentioned explicitly.
#
#Read the comments below for hints and directions.
##################################################################
##################################################################

class View:
    _MSG_LOG_LENGTH=5 #Number of messages to retain in view
    _SCREEN_WIDTH=300
    _SCREEN_HEIGHT=600
    _LINE_SPACING=round(_SCREEN_HEIGHT/2/(_MSG_LOG_LENGTH+1))

    def __init__(self,username='Me',partner_name='Partner'):
        self.username=username
        self.partner_name=partner_name
        self.my_client= Client()
        turtle.setup (width=200, height=200, startx=0, starty=0)
        self.msg_queue=[]
        self.oldmsg=turtle.clone()
        self.textbox=TextBox()
        self.sendbutton=SendButton(self)
        self.setup_listeners()

    def send_msg(self):
        
        '''
        You should implement (finish) this method.
        1) It should call the send() method of the Client object stored
        in this View instance.
        2) It should also call update the list of messages,
        self.msg_queue, to include this message.
        3) It should clear the textbox text display (show)
        (hint: use the clear_msg method).
        4) It should call self.display_msg() to cause the message
        display to be updated.
        '''
        self.my_client.send(self.textbox.new_msg)
        self.msg_queue.append(self.textbox.new_msg)
        self.textbox.clear_msg()
        self.display_msg()
        
        

    def get_msg(self):
        return self.textbox.get_msg()

    def setup_listeners(self):
        #return self.send_btn.fun()
        #turtle.listen()
        pass
        
        
        '''
        Set up send button - additional listener, in addition to click,
        so that return button will send a message.
        To do this, you will use the turtle.onkeypress function.
        The function that it will take is
        self.send_btn.fun
        where send_btn is the name of your button instance

        Then, it can call turtle.listen()
        '''
       

    def msg_received(self,msg):
        '''
        This method is called when a new message is received.
        It should update the log (queue) of messages, and cause
        the view of the messages to be updated in the display.

        :param msg: a string containing the message received
                    - this should be displayed on the screen
        '''
        
        print(msg) #Debug - print message
        show_this_msg=self.partner_name+' says:\r'+ msg
        #Add the message to the queue either using insert (to put at the beginning)
        #or append (to put at the end).
        #
        self.msg_queue.append(msg)
        #Then, call the display_msg method to update the display
        self.display_msg()
        

    def display_msg(self):
        '''
        This method should update the messages displayed in the screen.
        You can get the messages you want from self.msg_queue
        '''
        self.oldmsg.clear()
        self.oldmsg.write(self.msg_queue[-1])
        
##############################################################
##############################################################


#########################################################
#Leave the code below for now - you can play around with#
#it once you have a working view, trying to run you chat#
#view in different ways.                                #
#########################################################
if __name__ == '__main__':
    my_view=View('Einav')
    _WAIT_TIME=200 #Time between check for new message, ms
    def check() :
        msg_in=my_view.my_client.receive()
        if not(msg_in is None):
            if msg_in==Client._END_MSG:
                print('End message received')
                sys.exit()
            else:
                my_view.msg_received(msg_in)
        turtle.ontimer(check,_WAIT_TIME) #Check recursively
    check()
    turtle.mainloop()
