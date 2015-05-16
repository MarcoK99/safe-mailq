#!/usr/bin/env python


import sys
import time
from subprocess import Popen, PIPE, STDOUT
import subprocess
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from daemon import Daemon

if 'stop' == sys.argv[1]:
        print "Script stopped!"
else:
        pass

cmd = "mailq | egrep \'^--\'"
p = Popen(cmd, shell=True,  stdin=PIPE, stdout=PIPE, stderr=STDOUT)
output = p.stdout.read()
ctime = time.ctime()
print "Script is starting...\n"
print "Do you want to enter your own max. amount of emails in mailq? (recommended for huge servers!) \n"
yn2 = raw_input("Enter (y)es or (n)o: ")
checkerfmaom = None
if yn2 == "yes" or yn2 == "y":
        maom =  raw_input("Enter the max. amount of mails: ")
        checkerfmaom = True

elif yn2 == "no" or yn2 == "n":
        print"\n"
else:
        print"E: You have to enter yes/y or no/n!"
        sys.exit()

cmd2 = raw_input("Enter the shell command that would flush your mailq: ")

if len(cmd2) < 4:
        print "E: You need to enter the shell command that would flush your mailq!"
        sys.exit()

else:
        print "\nThe script will probably not work if you do not enter the correct command!"

print "\n"
print "Do you want to send a notification email when the mailq has been cleared? \n "

yn = raw_input("Enter (y)es or (n)o: ")

if yn == "yes" or yn == "y":
        print "Now enter the credentials for the sender of the notification email! \n"
        smtpserver = raw_input("--> Enter the SMTP server ip from where you want to send the notification email: \n ")

        if "." in smtpserver and len(smtpserver) >= 5:
                ssmtpport = raw_input("--> Enter the SMTP port from where you want to send the notification email: \n")
                smtpport = int(ssmtpport)
        else:
                print "E: You need to enter the SMTP server ip!"
                sys.exit()

        if isinstance(smtpport, basestring):
                print "E: You need to enter a SMTP port!"
                sys.exit()
        else:
                fromaddr = raw_input("--> Enter the sender email from the notification email: \n")

        if "@" in fromaddr and len(fromaddr) >= 5:
                fromaddr_pw = raw_input("--> Enter the password for the email address you entered: \n")
                checker = True
        else:
                print "E: You need to enter the sender email address when you want to recieve an email!"
                sys.exit()

        if len(fromaddr_pw) >= 3:
                toaddr = raw_input("--> Enter the adress where the notification email should be sent to: \n ")
        else:
                print "E: You need to enter the sender emails password when you want to recieve an email!"
                sys.exit()

        if "@" in toaddr and len(toaddr) >= 5:
                print "..."

elif yn == "no" or yn == "n":
         print "loading...\n"
else:
        print "The script has been terminated, make sure to enter yes / y or no / n"
        sys.exit()


print "The script is running as a daemon now, important information will be safed in mailqlog.txt"
ctime = time.ctime()

class MyDaemon(Daemon):
        def run(self):
                try:
                        def get_current_mails():
                                emails = []

                                try:
                                        for line in output.split(" "):
                                                emails.insert(0, line)
                                        mails_in_q_atm = int(emails[1])
                                        file_open = open("mmq.txt", "a")
                                        file_open.write('%s\n', (mails_in_q_atm))
                                        file_open.close()

                                except IndexError:
                                        f = open("mailqlog.txt", "a")
                                        f.write(str(ctime))
                                        f.write('There are currently no mails in mailq.\n')
                                        f.close()
                                        file_open = open("mmq.txt", "a")
                                        file_open.write('0\n')
                                        file_open.close()

                                time.sleep(1)


                        def read_mails_n_shutdown():

                                with open('mmq.txt', 'r') as infile:
                                        data =infile.read()
                                my_list = data.splitlines()

                                try:
                                        intlist = [int(i) for i in my_list]
                                        hour_mails = intlist[-1] + intlist[-2] + intlist[-3] + intlist[-4] + intlist[-5] + intlist[-6]
                                        hour_mails2 = intlist[-7] + intlist[-8] + intlist[-9] + intlist[-10] + intlist[-11] + intlist[-12]

                                        if checkerfmaom:

                                                if intlist[-1] >= intlist[-2] *1000 or intlist[-1] >= maom:
                                                        subprocess.Popen(cmd2, shell=True)
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('Mailq has been cleared (!) \n')
                                                        f.close()
                                                        checker = True
                                                        if checker:
                                                                try:
                                                                        msg = MIMEMultipart()
                                                                        msg['From'] = fromaddr
                                                                        msg['To'] = toaddr
                                                                        msg['Subject'] = "Mailqueues traffic is above the average."
                                                                        body = "Take a look at your mailqueue or at the log!"
                                                                        msg.attach(MIMEText(body, 'plain'))
                                                                        server = smtplib.SMTP('localhost', 587)
                                                                        server.ehlo()
                                                                        server.starttls()
                                                                        server.ehlo()
                                                                        server.login(fromaddr, fromaddr_pw)
                                                                        text = msg.as_string()
                                                                        server.sendmail(fromaddr, toaddr, text)
                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('A notification email has been sent!\n')
                                                                        f.close()


                                                                except IndexError:

                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('Mailq has been cleared (!) \n')
                                                                        f.close()

                                                                except NameError:
                                                                        palceholder = "lel"

                                                elif hour_mails >= hour_mails2 * 9:
                                                        subprocess.Popen(cmd2, shell=True)
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('The mailq has been cleared! \n')
                                                        f.close()
                                                        checker = True
                                                        if checker:
                                                                try:
                                                                        msg = MIMEMultipart()
                                                                        msg['From'] = fromaddr
                                                                        msg['To'] = toaddr
                                                                        msg['Subject'] = "Mailqueues traffic is above the average."
                                                                        body = "Take a look at your mailqueue please!"
                                                                        msg.attach(MIMEText(body, 'plain'))
                                                                        server = smtplib.SMTP('localhost', 587)
                                                                        server.ehlo()
                                                                        server.starttls()
                                                                        server.ehlo()
                                                                        server.login(fromaddr, fromaddr_pw)
                                                                        text = msg.as_string()
                                                                        server.sendmail(fromaddr, toaddr, text)
                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('--- !!! NOTIFICATION EMAIL HAS BEEN SENT!!!  ---\n')
                                                                        f.close()


                                                                except IndexError:

                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('Mailq has been cleared (!) \n')
                                                                        f.close()

                                                                except NameError:
                                                                        placeholer = kodmkdas



                                                else:
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('Mailq seems okay.\n')
                                                        f.close()

                                        else:

                                                if intlist[-2] != 1:
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('Mailq seems okay.\n')
                                                        f.close()


                                                elif hour_mails >= hour_mails2 * 9:
                                                        subprocess.Popen(cmd2, shell=True)
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('Mailq has been cleared (!)\n')
                                                        f.close()
                                                        checker = Trze
                                                        if checker:
                                                                try:
                                                                        msg = MIMEMultipart()
                                                                        msg['From'] = fromaddr
                                                                        msg['To'] = toaddr
                                                                        msg['Subject'] = "Mailqueues traffic is above the average."
                                                                        body = "Take a look at your mailqueue!"
                                                                        msg.attach(MIMEText(body, 'plain'))
                                                                        server = smtplib.SMTP('localhost', 587)
                                                                        server.ehlo()
                                                                        server.starttls()
                                                                        server.ehlo()
                                                                        server.login(fromaddr, fromaddr_pw)
                                                                        text = msg.as_string()
                                                                        server.sendmail(fromaddr, toaddr, text)
                                                                        f = open("mailq.log", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('Notification emails has been sent (!)\n')
                                                                        f.close()


                                                                except IndexError:

                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('Mailq has been cleared (!) \n')
                                                                        f.close()

                                                                except NameError:
                                                                         placeholer = kodmkdas


                                                elif intlist[-1] >= intlist[-2] * 6:
                                                        subprocess.Popen(cmd2, shell=True)
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('Mailq has been cleared (!) \n')
                                                        f.close()
                                                        checker = True
                                                        if checker:
                                                                try:
                                                                        msg = MIMEMultipart()
                                                                        msg['From'] = fromaddr
                                                                        msg['To'] = toaddr
                                                                        msg['Subject'] = "Mailqueues traffic is above the average."
                                                                        body = "Take a look at your mailqueue!"
                                                                        msg.attach(MIMEText(body, 'plain'))
                                                                        server = smtplib.SMTP('localhost', 587)
                                                                        server.ehlo()
                                                                        server.starttls()
                                                                        server.ehlo()
                                                                        server.login(fromaddr, fromaddr_pw)
                                                                        text = msg.as_string()
                                                                        server.sendmail(fromaddr, toaddr, text)
                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('Notification email has been sent (!)')
                                                                        f.close()


                                                                except IndexError:

                                                                        f = open("mailqlog.txt", "a")
                                                                        f.write(str(ctime))
                                                                        f.write('Mailq has been cleared (!) \n')
                                                                        f.close()

                                                                except NameError:
                                                                        placeholer = kodmkdas

                                                else:
                                                        f = open("mailqlog.txt", "a")
                                                        f.write(str(ctime))
                                                        f.write('Mailq seems okay. ')
                                                        f.close()


                                        time.sleep(5)


                                except IndexError:
                                         f = open("mailqlog.txt", "a")
                                         f.write(str(ctime))
                                         f.write('\n')
                                         f.close()


                                except ValueError:
                                         f = open("mailqlog.txt", "a")
                                         f.write(str(ctime))
                                         f.write('No or not enough mails in mailq\n')
                                         f.close()
                except:
                        print "shit"

                while True:
                        time.sleep(1)
                        get_current_mails()
                        read_mails_n_shutdown()

if __name__ == "__main__":
        daemon = MyDaemon('/tmp/mailqc.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
