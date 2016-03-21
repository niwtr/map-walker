'''
Mailer, a module communication protocol.
Current version: 0.1 2016/3/21
Design: Heranort
'''



'''
Mail generator.
First we should make sure what a mail is, especially in this program :)
A mail is a message that describes what the receiver is supposed to behave.
A mail contains: 
  1. a description of who sent it, namingly, tag.
  2. message that describes what the receiver should do.

Moreover, we don't want each of the receiver of the message to have its own
interpreter to translate the message into its own words. Thus we just define
the message to the *calling action* of a function. Instead of calling the 
functions of the receiver module directly, it sends the *action of calling*
to the receiver and let that guy judge wether to call. 

The meaning of this behavior is, giving the right of *doing things* to the 
receiver module itself, rather than let the sender take charge.

##
tag: tag of the sender of that mail.
func: function of the receiver module.
args: arguments of the function.
##

%%
________________________________________________________________________________
the_tag: return the tag of that sender.
________________________________________________________________________________
dispatch: dispatcher of the methods.

Never used directly by users.
________________________________________________________________________________
call: call the function.
________________________________________________________________________________
ex. 
def plus3(a,b,c):
    return a+b+c
a_mail=mail("hello, world",plus3,1,2,3)

a_mail(c
>>6
a_mail.the_tag()
>>"hello, world"
________________________________________________________________________________
%%
'''

def mail(tag, func, *args):
    def call():
        return func(*args)
    def the_tag():
        return tag
    def dispatch(method=0):
        if method=='tag':
            return tag
        else: 
            return call()
    return dispatch



'''
We use mailbox to serve as a pipe(or interface, if you like) that connects 
different modules. 
Contains a list, in fact, a queue, that preserves mails sent by other modules.
When a module (especially core module) was initialized, a mailbox should be 
attached to it, when the module wants to listen to other modules, it checks 
its maillist, get the message and do the behavior required. And when it wants
to talk to other modules, it takes the send() method to send messages to that 
module.

This term of model ensures the uniqueness and clearness of interfaces between 
any two modules. Besides, it allows tracking of message communication, which 
is absolutely convenient for debugging and testing.

##
maillist: messages to be read,
##

%%
________________________________________________________________________________
read: read the first message before trashing and do the required behavior.

ex. core.mailbox.read()
________________________________________________________________________________
send: push the required message to the mailbox of *other* module.

ex. If the core wants to talk to the route module to calculate the shortest path,
 it does:
core.mailbox.send(route.mailbox, FUNCTION_SHORTEST_PATH, "Changsha", "Wuhan")
**The message was described above.**
________________________________________________________________________________
display_mails: display the messages got and do nothing.

ex. core.mailbox.display_mails()
________________________________________________________________________________
read_all:read all the mails.
________________________________________________________________________________
%%

Design: Heranort
'''

class mailbox():
    
    maillist=[]
    mail_address=""
    
    def __init__(self, mail_address):
        self.mail_address=mail_address
        
    def get_mail_address(self):
        return self.mail_address

    def read(self, arg=0):
        if(len(self.maillist)!=0):
            self.maillist.pop(0)(arg)

    def read_all(self, args=[]):
        for mail in self.maillist:
            if (args!=[]):
                mail(args.pop(0))
            else:
                mail()
        self.maillist.clear()
        
    def get_mail(self,msg):    
        self.maillist.append(msg)

    def send(self,mailb,*msg):
        mailb.get_mail(mail(self.get_mail_address(),*msg))

    def display_mails(self):
        for mail in self.maillist:
            print ("Mail",mail,"from", mail('tag'))



##testing.
maila=mailbox('maila')
mailb=mailbox('mailb')
maila.send(mailb, print, "hello", "world1")
maila.send(mailb, print, "hello", "world2")
maila.send(mailb, print, "hello", "world3")
maila.send(mailb, print, "hello", "world4")
maila.send(mailb, print, "hello", "world5")
mailb.display_mails()
mailb.read()
mailb.display_mails()
mailb.read_all([1,'tag'])
