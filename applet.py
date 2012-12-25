#! /usr/bin/env python
import sys
import gtk
import appindicator
import paramiko
import subprocess

# configuration options for ssh connection
username = "myuser"
password = "mypass"
host = "computerhostname"

# change this to edit the applets name
app_name = "SSH Control"

class Commands:
    def __init__(self, title="Unknown", command=""):
        self.title = title
        self.command = command

commandArr = [];
# copy these down to make more options, the first arguement is the menu name, and the second the command to execute
commandArr.append(Commands("Play/Pause","./scripts/bs p"))
commandArr.append(Commands("Next Track","./scripts/bs n"))

class RemoteApplet:
    def __init__(self):
        self.ind = appindicator.Indicator("petteri",
                                           "petteri",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_label(app_name)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("new-messages-red")

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()
        self.command_items = []
        cnt = 0
        for x in commandArr:
            self.command_items.append(gtk.MenuItem(x.title))
            self.command_items[-1].connect("activate", self.handleitem, cnt)
            self.command_items[-1].show()
            self.menu.append(self.command_items[-1])
            cnt += 1
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.login()
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def login(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=username, password=password)

    def handleitem(self, widget, index):
        print "Running... " + commandArr[index].command
        stdin, stdout, stderr = self.ssh.exec_command(commandArr[index].command)

if __name__ == "__main__":
    indicator = RemoteApplet()
    indicator.main()
