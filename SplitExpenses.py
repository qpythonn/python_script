"""
This smal script aims at resolving split expenses between friends.
This is especially usefull to buy a nice present for Sylvain who decided that, for some reason, he was bored of seeing our face(s).
It takes a single argument which is a dictionnary containing the name of each participant  with the corresponding amount spent.

qpython 06.11.2016 
"""


# standard import
import operator


# example dicitionary {"name of the person 1" : amount spent by 1 , "name of the person 2" : amount spent by 2, ... }
spent_dict = {"Hana" : 90, "Quentin" : 80, "Akis" : 50 , "Olivier Speech Writer Smith" : 20, "Iris" : 60 }


# Total spent
total = float(sum(spent_dict.values()))
print "The total amount spent is " , total

# Average
n = len(spent_dict) # number of participants
average = total/n 
print "On average each person should have spent " , average


# The balance is defined as the amount spent - average
# If the balance is positive, the person should receive monney
balance_dict = {}
positive_dict = {}
negative_dict = {}

# loop over the fist dictionary to make calculate the balance and do the splitting
for key in spent_dict:
    balance = spent_dict[key] - average
    print "name of the person is " , key , " and the balance is ",  balance
    balance_dict[key] = balance
    # split the balance dict in two sub dict
    if ( balance > 0) :
        positive_dict[key] = balance
    elif (balance < 0) :
        negative_dict[key] = abs(balance)
    else :
        print key, "is already fair and do not have to send or receive monney !!!"


# sort the dictionary first
sorted_positive_dict = sorted(positive_dict.items(), key=operator.itemgetter(1))
sorted_negative_dict = sorted(negative_dict.items(), key=operator.itemgetter(1))


# some printout to make sure everythig is alright        
if (False):
    print " balance_dict is "
    print balance_dict
    
    print "positive_dict is "
    print positive_dict
    
    print "sorted_positive_dict is "
    print sorted_positive_dict
    
    print "negative_dict is "
    print negative_dict
    
    print "sorted_negative_dict is "
    print sorted_negative_dict



# remove first element of the dict till one of them is empty
transactions_list = []
counter = 0
while len(positive_dict) != 0 and len(negative_dict) != 0 :

    # define convenient variable
    first_neg = negative_dict.values()[0]
    first_pos = positive_dict.values()[0]
    first_key_neg = negative_dict.keys()[0]
    first_key_pos = positive_dict.keys()[0]
    
    # diff and min
    diff = abs(first_neg - first_pos)
    minimum = min(first_neg, first_pos)

    # start the logic
    if  (first_neg < first_pos ) :
        print first_key_neg , " gives  " , minimum , " to " , first_key_pos , " and is now fair!" 
        del negative_dict[first_key_neg]
        
        print first_key_pos , " should still receive " , diff
        positive_dict[first_key_pos] = diff
        


    elif (first_neg > first_pos) :
        print first_key_neg , " gives  " , minimum , " to " , first_key_pos , "but he still owes " , diff
        negative_dict[first_key_neg] = diff

        print first_key_pos , " is now fair !"
        del positive_dict[first_key_pos]

    else :
        print first_key_neg , " gives  " , minimum , " to " , first_key_pos , " and is now fair!"
        del negative_dict[first_key_neg]
        
        print first_key_pos , " is now fair !"
        del positive_dict[first_key_pos]


    transactions_list.append(first_key_neg + " gives  " + str(minimum) + " to " + first_key_pos)

    print "still owing monney ... "
    print negative_dict
    
    print "should still receive monney ... " 
    print positive_dict


    counter += 1


print "There is " , counter , " transactions to be done !!! "
print "These transactions are ... "

# loop over the list of transaction
for i, el in enumerate(transactions_list) :
    print i+1,")" , transactions_list[i]
    


    
