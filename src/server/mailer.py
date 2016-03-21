'''
Mailer, a module communication protocol.
Current version: 0.2 2016/3/21
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

a_mail(c(
>>6)
a_mail.the_tag()
>>"hello, world"
________________________________________________________________________________
%%
'''

def mail(tag, func, *args):
    
    def call():
        return func(*args)
    def showtag():
        return tag
    def describe():
        return (func, args)
    def do_not_call():
        pass
    
    def dispatch(method=0):
        if (method=='tag'):
            return showtag()
        elif (method=='describe'):
            return describe()
        elif (method=='pass'):
            return do_not_call()
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

The only con of this mechanism is that it is preserved only for side-effect
procedures, not for functions.
##
maillist: messages to be read,
##

%%
________________________________________________________________________________
read: read the first message before trashing and do the required behavior.

ex. core.mailbox.read()
________________________________________________________________________________
check: read the first message and do not destroy.
ex. core.mailbox.check()
________________________________________________________________________________
pread: (read and preserve) read the first message and preserve it in history.
ex.core.mailbox.pread()
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
    history=[]
    history_len=10
    mail_address=""
    
    def __init__(self, mail_address, history_len=10):
        self.mail_address=mail_address
        self.history_len=history_len
        
    def get_mail_address(self):
        return self.mail_address

    def read(self, arg=0):
        if(len(self.maillist)!=0):
            self.maillist.pop(0)(arg)
            
    def pread(self, arg=0):
        if(len(self.maillist)!=0):
            closure=self.maillist.pop(0)            
        if (len(self.history)>self.history_len):
            self.history.pop(0)
        self.history.append(closure)
        closure(arg)
        
    def read_again(self, arg=0):
        if(len(self.history)!=0):
            self.history.pop(0)(arg)
            
    def check(self, arg=0):
        if(len(self.maillist)!=0):
            self.maillist[0](arg)
            
    def trash(self):
        if(len(self.maillist)!=0):
            self.maillist.pop(0)
            
    def preserve(self):
        if (len(self.maillist)!=0):
            closure=self.maillist.pop(0)
        self.history.append(closure)
        
    def read_all(self, args=[]):
        for mail in self.maillist:
            if (args!=[]):
                mail(args.pop(0))
            else:
                mail()
        self.maillist.clear()
        
    def clear_history(self):
        self.history.clear()

    def read_all_history(self, args=[]):
        for mail in self.history:
            if(args!=[]):
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
            print ("Mail from",mail('tag'),"with content",mail('describe'))
            
    def display_histroy(self):
        for mail in self.history:
            print("History mail from",mail('tag'),"with content",mail('describe'))


##testing.



'''
maila=mailbox('maila')
mailb=mailbox('mailb')

maila.send(mailb, print, "hello", "world1")
maila.send(mailb, print, "hello", "world2")
maila.send(mailb, print, "hello", "world3")
maila.send(mailb, print, "hello", "world4")
maila.send(mailb, print, "hello", "world5")
mailb.display_mails()
mailb.pread()
mailb.display_mails()
mailb.pread()
mailb.trash()
mailb.read_all([1,'tag'])
mailb.display_histroy()
mailb.read_all_history()
'''