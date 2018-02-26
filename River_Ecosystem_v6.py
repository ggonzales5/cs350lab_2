#--------------------------------------------------#
# Program: CS350 LAB 1 Bear and Fish Ecosystem     #
# Author: Michael Gonzales                         #
# Date: 2-7-18                                     #
# Compilation: python River_Ecosystem_v5.py | less #
#                                                  #
# Description: This program simulates a river      #
# ecosystem comprised of Bears and Fish. This      #
# program utilizes object oriented                 #
# programming techniques, such as modularity       #
# abstraction, and encapsulation.                  #
# Note that this program strays slightly from      #
# the description particulary where the            #
# instructions were to change the river ecosystem  #
# for each animal object from the unmodified state #
# I wanted to experiment what would happen if the  #
# assignment was implemented with respect to time  #
# so as to nullify the scenarios where for example #
# if a fish A in cell [2] was eaten by Bear B in   #
# cell [1] in the step before, how is it that fish #
# A still exists for other animals in the          #
# unmodified state. This would mean the fish       #
# exists in multiple realities which just gets     #
# more confusing. So if the fish was eaten at time #
# step n then he is no longer in the environment   #
# at time step n+1 for the next animal. Now if we  #
# implement the algorithm with this modification   #
# must prevent a single animal from sweeping the   #
# entire board one time step after another. This   #
# can be handled by keeping track of "turns" at    #
# each epoch. If the animal had a turn it cant go  #
# again for that epoch. This is signified as a "1" #
# printed next to animals that have had their turn #
# So for example lets say that Bear at position    #
# [0] moved to position [1] when we move on to     #
# look at position [1] he cant get another turn    #
# which would possibly allow him to move forward   #
# again or perform some other action. Also, if we  #
# constantly just iterate through the river        #
# ecosystem starting at 0 to n then we give an     #
# advantaged bias to the first animal in the       #
# river, and so on and so forth. To alleviate this,#
# we can shuffle how we give each animal a turn at #
# each epoch.                                      #
#--------------------------------------------------#

import random
from random import shuffle
import types

#------------------------#
# Create an Animal Class #
# that will become the   #
# parent of the child    #
# classes, Bear and Fish #
#------------------------#
class Animal:

    #Constructor of the parent class Animal
    def __init__(self,movement=0):
        self.__turn = movement

    #Method: determines class name
    def getClassName(self):
        return self.__class__.__name__

    #Method: set movement marker instance
    #variable, 0 animal has not taken a turn
    #and 1 animal has taken a turn
    def setTurn(self,val):
        self.__turn = val

    def getTurn(self):
        return self.__turn

#-----------------------------------#
# Create a Bear Class that inherits #
# from class Animal                 #
#-----------------------------------#
class Bear(Animal):

    #Constructor inherits instance variables
    #from the superclass calling Animal.__init__(self)
    def __init__(self):
        Animal.__init__(self)
#-----------------------------------#
# Create a Fish Class that inherits #
# from class Animal                 #
#-----------------------------------#
class Fish(Animal):

   #Constructor inherits instance variables
   #from the superclass calling Animal.__init__(self)
   def __init__(self):
        Animal.__init__(self)

#-----------------------------------#
# Create a River Class that will    #
# dynamically add and remove Fish   #
# and Bear objects from the river   #
# class ecosystem.                  #
#-----------------------------------#
class River:

    #Constructor initialise river with
    #a random number of fish and bears
    #such that the river is 50% full
    def __init__(self,list_length):

        #Instantiate river to a user specified size
        self.__length = list_length
        self.__riverContents = [None] * self.__length

        #Fill only 50% of list with animals randomly
        for i in range(self.__length/2):

            #Get a random integer, either a 1 or a 2.
            randomAnimal = random.randint(1,2)

            #Add a Fish to the river if value is a 1
            if randomAnimal == 1:
                self.__riverContents[i] = Fish()

            #Add a Bear to the river if value is 2
            else:
                self.__riverContents[i] = Bear()

        #Shuffle the river contents so we dont
        #have all our animals in the first half
        #of the list.
        shuffle(self.__riverContents)

    #Method: Get the length of the river
    def getLen(self):
        return self._length

    #Method: Figure out what Animal object is in the kth
    #position of the river
    def getItem(self,k):
        return self.__riverContents[k]

    #Private Method: Set an Animal object in the River
    def setItem(self,k,obj):
        self.__riverContents[k] = obj

    #Private Method: Count the number of free spaces in the river
    def __getFreeRiverSpace(self):
        return self.__riverContents.count(None)

    #Private Method: Add an animal to the river only if we have free space
    def __addAnimal(self,animal):

        #Make sure the newly spawned animal
        #actually has empty river space to spawn.
        if self.__getFreeRiverSpace() > 0:

            #Create a list of indexes that represent
            #empty positions for animals to spawn
            position = []
            for index, obj in enumerate(self.__riverContents):
                if obj is None:
                    position.append(index)

            #Get a random index for the spawn point
            #and spawn the animal
            spawn_point = random.choice(position)
            self.setItem(spawn_point,animal)

            return spawn_point

    #Private Method: update a single animal position.
    def __updateAnimalPosition(self,k):

        #Change animal position only if the animal exists
        if self.__riverContents[k] is not None:

            #Roll die such that we can get a
            #-1,0 or 1 representing backward
            #static or forward movement.
            animal_move = random.randint(-1,1)

            #Okay the animal can move forward or backward in list
            #unless it is at the beginning or end of the list, then it
            #can only move forward or backward respectively, or stay put.

            #If the animal is going to move forward or backward
            #and if the animal is not in the 0th index position
            #and is attempting to move back or the animal is not
            #in the (self.__length - 1th) index position attempting
            #to move forward then go ahead and let the animal move.
            #Else that animal has to stay put by default because it
            #is at the edge of the river.
            if (animal_move != 0) and (0 <= k + animal_move < self.__length):

                #Move: into position if no animal is occupying the position.
                if self.__riverContents[k + animal_move] is None:

                    self.__riverContents[k + animal_move] = self.__riverContents[k]

                    #Print and set the movement field to keep track of animal attempted or actual movement
                    print "%s at postion [%d] %s" % (self.__riverContents[k].getClassName(),k, self.__getMovementString(animal_move))
                    self.__riverContents[k].setTurn(1)
                    self.__riverContents[k] = None

                #If the animals are the same type, create a baby animal only if space exists, and hold position of parents.
                elif ((self.__riverContents[k].getClassName() == self.__riverContents[k + animal_move].getClassName()) and (self.__getFreeRiverSpace() is not 0)):

                    #Add a baby bear cub :)
                    if self.__riverContents[k].getClassName() == "Bear":
                        spawn_point = self.__addAnimal(Bear())
                        print "Bear Created at position [%d]" % spawn_point

                    #Add a tiny tiny fish :)
                    else:
                        spawn_point = self.__addAnimal(Fish())
                        print "Fish Created at position [%d]" % spawn_point

                    #Set the turn field to 1
                    self.__riverContents[k].setTurn(1)
                    print "%s at position [%d] tried to %s" % (self.__riverContents[k].getClassName(),k,self.__getMovementString(animal_move))

                    #By default "birth" is considered a turn for the baby, so 1.
                    self.__riverContents[spawn_point].setTurn(1)

                #If this condition is met this means a bear has met a fish,
                #or fish has met a bear.... the fisssssh must DIEEEE!!!!
                else:

                    #If a bear has moved onto a fish position
                    if self.__riverContents[k].getClassName() == "Bear":

                        #Set turn field then move the Bear
                        self.__riverContents[k].setTurn(1)
                        self.__riverContents[k + animal_move] = self.__riverContents[k]

                        #Notify fish has been killed at the k + animal_move position and bear has moved
                        print "%s at position [%d] %s" % (self.__riverContents[k].getClassName(),k,self.__getMovementString(animal_move))
                        print "Fish at position [%d] has been eaten" % (k + animal_move)

                        #Remove bear from previous position
                        self.__riverContents[k] = None

                    #If a fish tried to move onto a bear position
                    else:

                        #Print movement status for the fish, no need to set movement field the animal died.
                        print "%s at position [%d] %s" % (self.__riverContents[k].getClassName(),k,self.__getMovementString(animal_move))

                        #Notify fish has been killed at the kth position
                        print "Fish at position [%d] has been eaten" % k

                        #Kill the fish
                        self.__riverContents[k] = None
            else:

                #Print appropriate statement if animal stayed put
                if animal_move is 0:

                    #Set turn field to 1
                    self.__riverContents[k].setTurn(1)
                    print "%s at position [%d] %s" % (self.__riverContents[k].getClassName(),k,self.__getMovementString(animal_move))

                #Print appropriate statement if animal tried to move
                else:

                    #Set turn field to 1
                    self.__riverContents[k].setTurn(1)
                    print "%s at position [%d] tried to %s" % (self.__riverContents[k].getClassName(),k,self.__getMovementString(animal_move))

    #Private Method: get movement string for printing
    def __getMovementString(self,val):

        if val is 0:
            val_str = "stayed put"
        elif val is -1:
            val_str = "moved up"
        else:
            val_str = "moved down"
        return val_str

    #Private Method: Perform movement of all animals for the river
    def __updateRiverState(self):

        #Flush all turn state animal fields at each epoch.
        #Get a list of indexes representing the animals
        #in the river and shuffle the index list. This
        #eliminates bias for animals upstream being able
        #to constantly go first all the time, as well as
        #saves computational cycles by skipping blank cells.
        index_list = []
        for i, obj in enumerate(self.__riverContents):
            if obj is not None:
                obj.setTurn(0)
                index_list.append(i)
        shuffle(index_list)

        #Iterate through all the positions in the river
        #but only give an animal a turn if they have
        #not already had one. This helps maintain our
        #model of having a river ecosystem with respect
        #to time, but not allowing for a single animal
        #object to move forward and sweep the entire board.
        #Note this is a very verbose output
        #because I am printing at every timestep
        for i in index_list:
            if self.__riverContents[i].getTurn() is 0:
                self.__updateAnimalPosition(i)
                self.printEntireRiverState(i)

    #Public Method: Print out the entire current state of the river
    def printEntireRiverState(self,k):

        #Just some printing of all my cells
        for index, obj in enumerate(self.__riverContents):
            if obj is not None:
                if obj.getClassName() == "Bear":
                    if k == index:
                        print "[%d][ Bear ] <-" % (index)
                    else:
                        print "[%d][ Bear ] %d" % (index,obj.getTurn())
                elif obj.getClassName() == "Fish":
                    if k == index:
                        print "[%d][ Fish ] <-" % (index)
                    else:
                        print "[%d][ Fish ] %d" % (index,obj.getTurn())
            else:
                if k == index:
                    print "[%d][      ] <-" % index
                else:
                    print "[%d][      ]" % index
        print "\n"

    #Public Method: Run the simulation until a certain percentage of the river is full.
    def runSimulation(self,percentage,max_epochs):

        count = 0
        while True:
            #At each epoch check <= 25%  of the river empty, if so finish the program
            if self.__getFreeRiverSpace()/float(self.__length) <= (1 - percentage):
                print "Finished: River at least %f percent populated" % (percentage*100)
                break
            #If we reach max epochs also break
            elif count > max_epochs:
                print "Finished: Max epochs reached"
                break
            else:
                print "#---------Year:%d---------#\n" % (count + 1)
                self.__updateRiverState()
                count = count + 1

#Start the river simulation eco-system program
river = River(10)
print "The beginning :)\n"
river.printEntireRiverState(None)
river.runSimulation(0.75,1000)
