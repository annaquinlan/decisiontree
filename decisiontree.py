'''
decisiontree.py
note that this will work even for non-binary classifications
'''
import sys
import math
import scipy.stats

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python decisiontree.py name_of_file.txt')
        sys.exit(1)
    
    else:
        f = open(sys.argv[1], 'r')
        text = f.readlines()
        
        # get the column headers for attributes
        columns = text[0].strip('\n')
        splitted = columns.split('\t')
        attrs = splitted[0:-1]
        
        # store attributes in a dictionary: { attr_name : [column index, set(possible values)] }
        attr_dict = {}
        for i, a in enumerate(attrs):
            attr_dict[a] = [i, set([])]
        
        # parse each example into: [ [vals of each attribute], classification]
        data = text[1:]
        examples = []
        
        for line in data:
            cleanline = line.strip('\n')
            example = cleanline.split('\t')
            
            ex_attrs = example[0:-1]
            ex_classif = example[-1]
            
            examples.append([ex_attrs, ex_classif])
            
            ### keep track of all possible attribute values (in attr_dict)
            ### keep track of all possible classifications
            for i, a in enumerate(attrs):
                attr_dict[a][1].add(ex_attrs[i])
        
        # This is tree trained on all data.
        print_bool = True
        chisq_bool = False
        node = DTL(examples, attr_dict, [], 0, None, print_bool)
        
        # Tree trained on all examples except one
        denom = len(examples)
        num = 0.0
        print_bool = False
        for i, ex in enumerate(examples):
            subset = examples[0:i] + examples[i+1:]
            node = DTL(subset, attr_dict, [], 0, None, print_bool)
            print "--------"
            print i, str(ex)
            result = classify(ex, node, attr_dict)
            print result.classif
            if result.classif == ex[-1]:
                num += 1
        print "Accuracy on training set: ",
        n = (num*100.0)/denom
        print ( "%.2f" % n),
        print "%"
        
        '''
         # This is tree trained on all data.
        print_bool = True
        node = DTL(examples, attr_dict, [], 0, None, print_bool)
        
        # Prune tree
        chi_sq_tree
        # Tree trained on all examples except one
        chi_sq_num = 0.0
        print_bool = False
        for i, ex in enumerate(examples):
            subset = examples[0:i] + examples[i+1:]
            node = DTL(subset, attr_dict, [], 0, None, print_bool)
            print "--------"
            print i, str(ex)
            result = classify(ex, node, attr_dict)
            print result.classif
            if result.classif == ex[-1]:
                chi_sq_num += 1
        print "Accuracy on training set: ",
        chi_sq_n = (chi_sq_num*100.0)/denom
        print ( "%.2f" % chi_sq_n),
        print "%"
        
        if chi_sq_num > num:
            print "Chi-Square pruning improved accuracy by",
            print (chi_sq_n - n),
            print "%"
        '''
                
# Classifies data item by recursively traversing tree created by DTL, using item's attribute values to choose path
def classify(example, node, attr_dict):

    if isinstance(node, answer_node):
        return node
    
    ex_val_in = attr_dict[node.attr][0]
    ex_val = example[0][ex_val_in]
    
    for child in node.children:
        if child.value == ex_val:
            return classify(example, child, attr_dict)
        
# Implementation of decision tree learning algorithm, with printing
def DTL(examples, attr_dict, parents, count, value, print_bool):
    attributes = attr_dict.keys()
    
    # Case 1: If there are no more examples:
    if len(examples) == 0:
        
        classif = get_plurality(parents)[0]
        node = answer_node(classif, value)
        if print_bool:
            print ": " + classif
        return node
        
    # Case 2: All examples have the same classification:
    # Number of examples with the dominant classification is the same as the number of examples.
    elif get_plurality(examples)[1] == len(examples):
        
        # We'll just take the classification of the first example because they're all the same.
        classif = examples[0][-1]
        node = answer_node(classif, value)
        if print_bool:
            print ": " + classif
        return node
        
    # Case 3: If the attributes list is empty:
    elif len(attributes) == 0:
        classif = get_plurality(examples)[0]
        node = answer_node(classif, value)
        if print_bool:
            print ": " + classif
        return node
    
    # Case 4: Recursive case. 
    else:
        if print_bool:
            print
        attr = get_best_attr(attr_dict, examples)
        node = choice_node(attr, value)
        values = list(attr_dict[attr][1])
        index = attr_dict[attr][0]
        
        # Sort examples by values of best attribute.
        exsbyvals_dict = {}
        for val in values:
            exsbyvals_dict[val] = []
        
        for ex in examples:
            exval = ex[0][index]
            exsbyvals_dict[exval].append(ex)
        
        # Delete best attribute from dictionary of attributes.
        subattr_dict = dict(attr_dict)
        del subattr_dict[attr]
        
        # Recurse on each group of split examples.
        for val in values:
            subexamples = exsbyvals_dict[val]
            if print_bool:
                print count*'| ' + str(attr) + " = " + str(val),
            child = DTL(subexamples, subattr_dict, examples, count+1, val, print_bool)
            node.children.append(child)

        return node
'''
# Implement chi-sq pruning
def prune(node):
    can_prune = True
    observed = []
    for child in node.children:
        if isinstance(child, choice_node):
            can_prune = False
        else:
'''           
            
        
# The classification of a group of split examples.
class answer_node:
    def __init__(self, classif, value):
        self.classif = classif
        self.value = value
        
    def __str__(self):
    	return self.classif

# The attribute split on and nodes resulting from the split.
class choice_node:
    def __init__(self, attr, value):
        self.attr = attr
        self.children = []
        self.value = value
        
    def __str__(self):
    	print "--- choice node ---"
    	print self.attr
    	for child in self.children:
    	    print "*"
    	return "---"

'''    	
def print_tree(node, attr_dict):
    if isinstance(node, answer_node):
        print ": " + str(node.classif)
    else:
        print node.attr
''' 

# Get_plurality returns classification with highest percentage given example list and possible 
# classifications. It also returns how many examples had that classification.
def get_plurality(ex_list):
   
    yes_ct = 0
    no_ct = 0
    
    for ex in ex_list:
        classif = ex[-1]
        if classif == "yes":
            yes_ct += 1
        else:
            no_ct += 1
    
    if yes_ct > no_ct:
        return 'yes', yes_ct
    else:
        return 'no', no_ct
    

def get_best_attr(attr_dict, examples):

    # get entropy of examples list
    yes_ct = 0.0
    no_ct = 0.0
    for ex in examples:
        classif = ex[-1]
        if classif == "yes":
            yes_ct += 1
        else:
            no_ct += 1
    entropy = get_entropy(yes_ct/(len(examples)))
    
    attributes = attr_dict.keys()
    max = 0
    best_attr = attributes[0]
    for attr in attributes:
        values = list(attr_dict[attr][1])
        index = attr_dict[attr][0]
        
        # Count examples with that value
        ex_ct_dict = {}
        for val in values:
            ex_ct_dict[val] = [0.0,0.0] # yes_ct, no_ct
        
        for ex in examples:
            exval = ex[0][index]
            exclassif = ex[1]
            if exclassif == "yes":
                ex_ct_dict[exval][0] += 1
            else:
                ex_ct_dict[exval][1] += 1
        
        remainder = 0
        for val in values:
            proportion = (ex_ct_dict[val][0] + ex_ct_dict[val][1])/len(examples)
            if ex_ct_dict[val][0] + ex_ct_dict[val][1] != 0:  
                q = ex_ct_dict[val][0]/(ex_ct_dict[val][0] + ex_ct_dict[val][1])
                if q != 0 and q != 1:
                    remainder += proportion * get_entropy(q)
                # else entropy is 0 -- nothing added to remainder
        
        gain = entropy - remainder
        if gain > max:
            max = gain
            best_attr = attr
    
    return best_attr
    
def get_entropy(q):
    return -q*math.log(q, 2) - (1 - q)*math.log((1 - q), 2)
    
if __name__ == "__main__":
    main()
    
    '''    
    else:
        attr = best attribute of examples and attributes
        make a choice node with that attribute
        for val in attr.getvalues()
            subexamples = [examples where attr has value val]
            subattributes = attributes - attr
            child = DTL(subexamples, subattr, examples]
            add child to node 
        return node
    '''