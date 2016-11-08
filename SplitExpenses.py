"""
This smal script aims at resolving split expanses between friends.
This is especially usefull to buy a nice present for Sylvain who decided that, for some reason, he was bored of seeing our face(s).
It takes a single argument which is a dictionnary containing the name of each participant  with the corresponding amount spent.

qpython 06.11.2016 
"""


# example dicitionary {"name of the person 1" : amount spent by 1 , "name of the person 2" : amount spent by 2, ... }
my_dict = {"Hana" : 100, "Quentin" : 50, "Akis" : 30 , "Olivier Speech Writter Smith" : 40 }


# Total spent
total = float(sum(my_dict.values()))
print "The total amount spent is " , total

# Average
n = len(my_dict) # number of participants
average = total/n 
print "On average each person should have spent " , average


# The balance is defined as the amount spent - average
# If the balance is positive, the person should receive monney

# Print balance for each person
for key in my_dict:
    print "name of the person is " , key , " and the balance is ",  my_dict[key] - average
