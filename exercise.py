""" 
Junior BE Challenge

Aim: Create a Class with a dictionary list with name, party, age, number 
(unique) and vote of each deputy in which it is possible to add and delete 
votes. Within this Class it should be possible to return a dictionary of 
total  of votes in favor, against and the total abstention. 
It should also be possible to retorn the total number of votes by political 
party and a list with the deputies names sorted by age (descendent) and, 
if they have the same age, sorted by name in ascendent order. 

This script requires that `pandas` and `numpy` be installed within the Python
environment you are running this script in.

"""

import  numpy as np
import pandas as pd


class MontijoVotes: 

    #Class that stores and returns information about deputies votes.
    
    _registry = []
    #List of dictionaries name, party, age, number and vote of each deputy

    def __new__(cls, name, party, age, number):
    """ Creates and stores new class instance for each candidate, checking for unique 
    deputy number values. 
    
    ------------------------------------
    Parameters (str): 
        name; party; age; number
    
    Returns:
     - Error if deputy number already exists
     - self if instance created sucessefuly 

    """
  
        if cls._registry:
        #Check if element with same number already exists. 
            for element in cls._registry:
                if number == element['number']:
                    #print Error if exists. 
                    return (print('Error: {0} deputy number already exists'.format(number)) )

        self = super().__new__(cls)

        self.name = name
        self.party = party
        self.age = age
        self.number = number
        self.vote = '-'
        
        #stores dictionary in class. 
        self._registry.append(self.__dict__)
        return self
    

    def addVote(self, value):
    """Function to add vote if no vote exists. 
    
    ------------------------------------
    Parameters: 
        self; value of vote (str);
        
    Returns (print):
        - Error if a vote already exists
        - Vote added successfully
    """
        if self.vote == '-':
            self.vote = str(value).lower()
            #print if sucesseful. 
            return(print('Vote added successfully'))
        else:
            #print error.
            return(print('Error: Already vote'))


    def removeVote(self):
    """Function to delete vote if vote exists. 
    
    ------------------------------------
    Parameters: 
        self;
        
    Returns (print):
        - Error if no vote found
        - Vote added successfully
    """
        if self.vote == '-':
            return (print('Error: No vote found'))
        else: 
            self.vote = '-'
            return (print('Vote deleted successfully')) 
    

    def checkKeys(self, series):
    """To avoid repeating code, this function receives a panda series and converts this
    Series to a dictionary with votes in favor, against and abstention.    
    ------------------------------------
    Parameters: 
        self; Panda Series. 
        
    Returns (dictionary):
        - {in_favor: , against: , abstention: }
    """
        votes = series
        final = {'in_favor': 0, 'against': 0, 'abstention': 0}
        if 'yes' in votes.keys(): 
            final['in_favor'] = votes['yes']
        else: 
            final['in_favor'] = 0
        if 'no' in votes.keys(): 
            final['against'] = votes['no']
        else: 
            final['against'] = 0
        if '-' in votes.keys():
            final['abstention'] = votes['-']
        else:
            final['abstention'] = 0
        return(final)
          

    def totalVotes(self):
    """Function to count the total number of votes returning a dictionary with total
    of votes in favor, against and the abstention     
    ------------------------------------
    Parameters: 
        self;
        
    Returns (dictionary):
        - {in_favor: , against: , abstention: }
    """
        deputies = pd.DataFrame(MontijoVotes._registry)
        votes = deputies['vote'].value_counts() #Count number of identical values in votes
        finalvotes = self.checkKeys(votes) #Organize the data in a final dictionary
        return (finalvotes)
    
    def partyVotes(self):
    """Function to count the total number of votes for each party returning a dictionary 
    with votes in favor, against and the abstention     
    ------------------------------------
    Parameters: 
        self;
        
    Returns (list of dictionaries):
        - [{PSD: {in_favor: , against: , abstention: }},{PS: {in_favor: , against: , abstention: }}] 
    """
        deputies = pd.DataFrame(MontijoVotes._registry)
        byparties = deputies.groupby('party')['vote'].value_counts()
        partynames = byparties.index.get_level_values(0).drop_duplicates() #Get the political party names to be used as key. 
        finalvotes = []
        for i in partynames:
            partyvotes = self.checkKeys(byparties[i])
            finalvotes.append({str(i) : partyvotes.copy()})
        print(finalvotes)
        
    
    def totalDeputies(self):
    """Function that returns a list of all deputies' names order by age (descendent) and, 
    if the age is the same, by name (ascendent)     
    ------------------------------------
    Parameters: 
        self;
        
    Returns (list):
        - Deputies names in a list
    """
        deputies = pd.DataFrame(MontijoVotes._registry).sort_values(by=['age','name'], ascending=[False, True])
        deputiesnames = deputies['name'].values
        return (deputiesnames)



