import csv

class matrix:
    
    def __init__(self):
        
        with open('FlyFrequency.csv','rb') as file:
            contents = csv.reader(file)
            fly = list()
            for row in contents:
                fly.append(row)
            
            for i in xrange(0,4):
                fly.pop(0)

essai=matrix()