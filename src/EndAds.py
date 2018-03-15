
# -*- coding: utf-8 -*-
#title           :PythonAdBlocker.py
#description     :This program is an alternative to adblocker or any software used to block ads.
#author          :Sonny Hu
#date            :2017/24/10
#version         /:1.2/
#notes           :Need admin privileges
#python_version  :3.6
#=======================================================================
 
# Import the modules needed to run the script.

import os
from bs4 import BeautifulSoup
from textwrap import wrap
import time
import sys
from win32com.shell import shell
import io
import requests

def isUserAdmin():
        if shell.IsUserAnAdmin():
                print("Admin user detected, can continue!")
        else:
                print("Standard user detected, cannot continue the execution! Need administrative privileges! Maybe you should run EndAds as administrator")
                time.sleep(3)
                sys.exit(0)
                
def progBar(curr, total, full_progbar):
        frac = curr/total
        filled_progbar = round(frac*full_progbar)
        print('\tComplete\r\tDoing=>', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')

def startProgBar():
        for i in range(4000+1):
                progBar(i, 4000, 25)
        print()

def writeIn(text, file):
	with io.open(file, "a+", encoding="utf-8") as f:
		f.write(text)		

def checkStatus():
        print("Checking status of http://someonewhocares.org/hosts")
        try:
                webPage = requests.get("http://someonewhocares.org/hosts/")
                status = webPage.status_code
                if  status == 200:
                        print("\t->HTTP 200")
                        return True
                else:
                        print("Unable to get data from http://someonewhocares.org/hosts\n\t HTTP %s" %(status))
        except requests.ConnectionError as e:
                print("Unable to get data from http://someonewhocares.org/hosts\n\t HTTP %s" %(status))
                return False
               
def makeHosts():
        #Get webPage
        webPage = requests.get("http://someonewhocares.org/hosts/")
        #Get Global info
        soup = BeautifulSoup(webPage.content, 'html.parser')
        soup.find_all(class_="BODY")
        data = soup.find_all(class_="BODY")
        dataGlobal = data[0].get_text()
        #Get Only needed info
        dataFinal = dataGlobal.rpartition('#<shock-sites>')[-1]
        dateUpdate="\n#Python EndAds version 1.2 (do not delete this line or else update will not function correctly). If you have other local DNS lookup, put them before this line\n#Last update: " + (dataGlobal.split('Last updated: ', 2)[1]).split('\n')[0] + "\n"
        return dateUpdate, dataFinal;

def getCurrentHosts():
        with open('C:\Windows\System32\drivers\etc\hosts', 'r') as myfile:
            dataCurrentHosts=myfile.read()
        return dataCurrentHosts;

def installCurrentHosts():
        print("hello")
        
def updateHosts():
        print("hello")

def delBackup():
        if (os.path.isfile("C:\Windows\System32\drivers\etc\hosts.bak")):
                open("C:\Windows\System32\drivers\etc\hosts.bak", 'w').close()
        
def doBackup():
        dataBackup = getCurrentHosts()
        writeIn("#Important file, use this if something wrong happened\n" + dataBackup, "C:\Windows\System32\drivers\etc\hosts.bak")
        
def removeHosts(file):
        hostsFile = file
        try:
                os.remove(file)
        except OSError as error:
                print(" ")
                #print("Error, %s - %s, will continue the operation"% (error.filename,error.strerror))

def printWithBorder(text, width):
        print('+-' + '-' * width + '-+')
        for line in wrap(text, width):
                print('| {0:^{1}} |'.format(line, width))
        print('+-' + '-'*(width) + '-+')

def checkHostsWin():
        if (os.path.isfile("C:\Windows\System32\drivers\etc\hosts")):
                return True
        else:
                return False
        
def checkIfInstalled() :
        if 'Python EndAds' in open("C:\Windows\System32\drivers\etc\hosts").read():
                return True;
        else:
                return False

def main_menu():
        os.system('cls')
        printWithBorder("====== EndAds ======", 100)
        #print(30 * "-" , "Python EndAds" , 30 * "-")
        print("1. Install -/- Update EndAds ")
        print("2. Perform backup (will overwrite if you already have a backup)")
        print("3. Just build hosts file")
        print("4. Help")
        print("5. About")
        print("Q|q. Quit\n")


isUserAdmin()
winHostsLocation = "C:\Windows\System32\drivers\etc\hosts"
loop = True
about = "EndAds is an alternative to adblock and any other softwares, add-ons or plugins used to block ads. No need to install any software or programs, this will use windows hosts file to block any known ads by preventing your computer from connecting to selected internet hosts. Again a great thanks to Dan Pollock and all people who keep submitting sites."
while loop:
        main_menu()
        choice = input("Enter what you want to do [1-5]:")
        if choice == "1":
                if checkHostsWin():
                        if checkIfInstalled():
                                if (checkStatus()):
                                        print("EndAds is already installed, update is going to be performed")
                                        time.sleep(1)
                                        with open(winHostsLocation, 'r') as myfile:
                                                #Get all contents before EnAds
                                            data=myfile.read().partition('#Python EndAds')[0]
                                                #Get new contents from someonewhocare
                                            print("Getting update from http://someonewhocares.org/hosts")
                                            startProgBar()
                                            dateUpdate, dataFinal = makeHosts()
                                            
                                                #Write in hosts file cleaned
                                        print("Updating windows hosts file")
                                        startProgBar()
                                        open(winHostsLocation, 'w').close()
                                        writeIn(data, winHostsLocation)
                                        writeIn(dateUpdate, winHostsLocation)
                                        writeIn(dataFinal, winHostsLocation)
                                        print("\n*****Updated successfully*****")
                                        input("\nPress any key to continue..")
                                else:
                                        input("Error while trying to update hosts file, Enter any key to try again..")
                                    
                                
                        else:
                                if (checkStatus()):
                                        print("Not installed, starting installation")
                                        time.sleep(1)
                                        #/\Get data from someonewhocares
                                        print("Getting data from http://someonewhocares.org/hosts/")
                                        startProgBar()
                                        dataCurrentHosts = getCurrentHosts()
                                        dateUpdate, dataFinal = makeHosts()
                                        #/\Backing up and deleting hosts file
                                        print("Backing up current hosts file")
                                        startProgBar()
                                        print("Deleting hosts file")
                                        startProgBar()
                                        doBackup()
                                        removeHosts(winHostsLocation)
                                        #/\Creating newhosts file
                                        print("Installing new hosts file")
                                        startProgBar()
                                        writeIn(dataCurrentHosts, winHostsLocation)
                                        writeIn(dateUpdate, winHostsLocation)
                                        writeIn(dataFinal, winHostsLocation)
                                        print("\n*****Installed successfully*****")
                                        input("\nPress any key to continue..")
                                else:
                                        input("Error while trying to install hosts file, Enter any key to try again..")
                else:
                        print("\nError, could not find windows hosts file, maybe missing, please, make sure windows hosts file exists..")
                        input("Enter any key to try again..")
                
        elif choice == "2":
                print("Backing up C:\\Windows\\System32\\drivers\\etc\\hosts")
                delBackup()
                doBackup()
                startProgBar()
                print("\n*****Done successfully*****")
                input("\nPress any key to continue..")
                
        elif choice == "3":
                if (checkStatus()):
                        print("Getting data from http://someonewhocares.org/hosts/")
                        startProgBar()
                        print("Building hosts file...")
                        removeHosts("hostsFile")
                        dateUpdate, dataFinal = makeHosts()
                        writeIn(dateUpdate, "hostsFile.txt")
                        writeIn(dataFinal, "hostsFile.txt")
                        startProgBar()
                        print("\n*****Job done, hosts file built*****")
                        input("\nPress any key to continue..")
                else:
                        input("Error while trying to build hosts file, Enter any key to try again..")
        elif choice == "4":
                printWithBorder("Not available yet", 50)
                input("Press any key to continue..")
        elif choice == "5":
                print("\nName: EndAds\nAuthor: Hu Sonny\nVersion: 1.2\n")
                printWithBorder("A great thanks to Dan Pollock and his team", 50)
                printWithBorder(about, 50)
                time.sleep(1)
                input("Press any key to continue..")
        elif choice == "q" or choice == "Q":
                print("See you")
                time.sleep(1)
                loop = False
        else:
                input("Wrong option selection. Enter any key to try again..")
os.system("pause")
