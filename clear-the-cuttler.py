#This program is used to rename the files whose u want to rename
from os import *
folder_path="/Users/hp/Desktop/garbage" #This is the  path of files
show=listdir(folder_path) #this is use convert the all files in the list
for i in range(0,len(show)):
  a=show[i] #this is use to send the image one one
  if(a.endswith(".jpeg")): #this is used to chk the file formate
    rename(a,f"{i}.jpeg") #this is use to rename the files