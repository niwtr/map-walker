#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Mailer, a module communication protocol.
Current version: 0.3 2016/3/22
Design: Heranort
'''

'''
**************************************NEWS**************************************
0.3:
Fixed return values (see test examples!)
********************************************************************************
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

>>6
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
display_history: display the preserved history.
ex. core.mailbox.display_mails()
________________________________________________________________________________
read_all:read all the mails and ignore.
read_all_history: read all the mails and clear history.
________________________________________________________________________________
preserve: preserve the mails in history.
trash: delete current mail.(unread)
________________________________________________________________________________
%%

Design: Heranort
'''

class mailbox():
    
    
#    maillist             #container of mails
    
#    history              #container of histories
    
#    history_len        #maximum length of history container
    
#    mail_address        #tag of the mailbox, can be showed in mails
    
    def __init__(self, mail_address, history_len=10):
        self.maillist=[]
        self.history=[]
        self.mail_address=mail_address
        self.history_len=history_len
        
    def get_mail_address(self):
        return self.mail_address

    #read and ignore.
    def read(self, arg=0):
        if(len(self.maillist)!=0):
            return self.maillist.pop(0)(arg)
    
    
    def clearp(self):
        return len(self.maillist)==0
        
    #read and preserve in history.       
    def pread(self, arg=0):
        if(len(self.maillist)!=0):
            closure=self.maillist.pop(0)
            if (len(self.history)>self.history_len):
                self.history.pop(0)
            self.history.append(closure)
            return closure(arg)
        else: 
            pass
    def npread(self, num=1,arg=0):
        while(num>0):
            print(num)
            if(len(self.maillist)!=0):
                closure=self.maillist.pop(0)
                if (len(self.history)>self.history_len):
                    self.history.pop(0)
                self.history.append(closure)
                closure(arg)
            else: 
                pass
            num=num-1
        
    def pread_all(self, args=[]):
        retv=[]
        for mail in self.maillist:
            if(len(self.history)>self.history_len):
                self.history.pop(0)
            self.history.append(mail)
            if(args!=[]):
                retv.append(mail(args.pop(0)))
            else: 
                retv.append(mail())
        self.maillist.clear()
        return retv

    
    
    #read the first history.    
    def read_again(self, arg=0):
        if(len(self.history)!=0):
            return self.history.pop(0)(arg)

    #simply excurte the mail.
    def check(self, arg=0):
        if not self.clearp():
            return self.maillist[0](arg)
        else : 
            return 'nil'
        
    
    #delete the mail.        
    def trash(self):
        if(len(self.maillist)!=0):
            self.maillist.pop(0)
    
    #do not read and preserve in history.        
    def preserve(self):
        if (len(self.maillist)!=0):
            closure=self.maillist.pop(0)
            self.history.append(closure)
    
    #read all of the mails and ignore.    
    def read_all(self, args=[]):
        retv=[]
        for mail in self.maillist:
            if (args!=[]):
                retv.append(mail(args.pop(0)))
            else:
                retv.append(mail())
        self.maillist.clear()
        return retv
    
    #delete all the histories     
    def clear_history(self):
        self.history.clear()

    #read all the histories, and clear.
    def read_all_history(self, args=[]):
        retv=[]
        for mail in self.history:
            if(args!=[]):
                retv.append(mail(args.pop(0)))
            else:
                retv.append(mail())
        self.maillist.clear()
        return retv
        
    def get_mail(self,msg):
        self.maillist.append(msg)

    #send mails to other mailbox
    def send(self, mailb, *msg):
        mailb.get_mail(mail(self.get_mail_address(),*msg))
        
    def send_mail(self, mailb, m):
        mailb.get_mail(m)

    def echo_bind(self, m):
        fr=m('tag')
        def echo(res):
            self.send(fr, lambda x:x, res)
        echomail=mail(fr,echo,m())
        return echomail




        
    #show all the mails in mailbox
    def display_mails(self,printf=print):
        for mail in self.maillist:
            printf ("##Mail from",mail('tag'),"with content",mail('describe'))

    #show all the mails in history.
    def display_histroy(self,printf=print):
        for mail in self.history:
            printf("##History mail from",mail('tag'),"with content",mail('describe'))

    def get_all_mails(self):
        return self.maillist
    
    def get_all_histories(self):
        return self.history

#test examples.
'''

def plusall(*args):
    def iiter(acc,args):
        if(len(args)==0):
            return acc
        else:
            return iiter(acc+args[0],args[1:])
    return iiter(0,args)

    
maila=mailbox('maila')
mailb=mailbox('mailb')

maila.send(mailb, print, "hello", "world")
maila.send(mailb,plusall, 1,2,3,4,5)
maila.send(mailb,plusall, 1,2,3,5)
maila.send(mailb,plusall, 1,2,4,5)
maila.send(mailb,plusall, 1,3,4,5)
maila.send(mailb,plusall, 2,3,4,5)
maila.send(mailb,plusall, 1,2,3)
maila.send(mailb,plusall, 3,4,5)

#mailb.display_mails()
mailb.pread()
mailb.display_histroy()

a=mailb.read()
mailb.preserve()
mailb.display_mails()
mailb.trash()
b=mailb.read_all([1,'tag'])
mailb.display_histroy()
c=mailb.read_all_history()
print("a=",a,"b=",b,"c=",c)
'''