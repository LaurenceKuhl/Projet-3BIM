import csv

class matrix:
    
    def __init__(self):

        with open('Population.csv','rb') as file:
            contents = csv.reader(file)
            pop = list()
            for row in contents:
                pop.append(row)
                
            for i in xrange(0,3):
                pop.pop(0)
                pop.pop(-1)
            pop.pop(0)
        
        with open('FlyFrequency.csv','rb') as file:
            contents = csv.reader(file)
            fly = list()
            for row in contents:
                fly.append(row)
            
            for i in xrange(0,4):
                fly.pop(0)

essai=matrix()