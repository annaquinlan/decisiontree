'''
decisiontree.py
note that this will work even for non-binary classifications
'''
import sys
import math
import scipy.stats
import numpy

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python decisiontree.py name_of_file.txt')
        sys.exit(1)
    
    else:
        f = open(sys.argv[1], 'r')
        text = f.readlines()
        f.close()
        
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
        print
        print "***Un-pruned tree, trained on all data:"
        node = DTL(examples, attr_dict, [], 0, None)
        print_tree(node, 0)
        
        denom = len(examples)
        # Accuracy on training set
        correct_alldata = 0.0
        for ex in examples:
            result = classify(ex, node, attr_dict)
            if result.classif == ex[-1]:
                correct_alldata += 1
        print "Accuracy (unpruned) on training set: ",
        accuracy_alldata = (correct_alldata*100.0)/denom
        print ( "%.2f" % accuracy_alldata),
        print "%"
        
        # Leave One Out
        correct_leaveoneout = 0.0
        for i, ex in enumerate(examples):
            subset = examples[0:i] + examples[i+1:]
            node = DTL(subset, attr_dict, [], 0, None)
            result = classify(ex, node, attr_dict)
            if result.classif == ex[-1]:
                correct_leaveoneout += 1
        print "Accuracy (unpruned) with leave-one-out cross-validation: ",
        accuracy_leaveoneout = (correct_leaveoneout*100.0)/denom
        print ( "%.2f" % accuracy_leaveoneout),
        print "%"
        
        
        # Prune tree
        prune(node)
        print
        print "***Pruned tree, trained on all data:"
        print_tree(node, 0)
        
        # Chi-Sq: accuracy on training set
        correct_alldata_chisq = 0.0
        for ex in examples:
            result = classify(ex, node, attr_dict)
            if result.classif == ex[-1]:
                correct_alldata_chisq += 1
        print
        print "Accuracy (pruned) on training set: ",
        accuracy_alldata_chisq = (correct_alldata_chisq*100.0)/denom
        print ( "%.2f" % accuracy_alldata_chisq),
        print "%"
        
        # Chi-Sq: Leave One Out
        chi_sq_num = 0.0
        for i, ex in enumerate(examples):
            subset = examples[0:i] + examples[i+1:]
            node = DTL(subset, attr_dict, [], 0, None)
            prune(node)
            result = classify(ex, node, attr_dict)
            if result.classif == ex[-1]:
                chi_sq_num += 1
        print
        print "Accuracy (pruned) with leave-one-out cross-validation: ",
        chi_sq_n = (chi_sq_num*100.0)/denom
        print ( "%.2f" % chi_sq_n),
        print "%"
        
        print
        if chi_sq_num > correct_leaveoneout:
            print "Chi-Square pruning improved leave-one-out accuracy by",
            print (chi_sq_n - accuracy_leaveoneout),
            print "%"
        elif chi_sq_num == correct_leaveoneout:
            print "Chi-Square pruning did not change leave-one-out accuracy."
        else:
            print "Chi-Square pruning reduced leave-one-out accuracy by",
            print (accuracy_leaveoneout - chi_sq_n),
            print "%"
        print
                
# Classifies data item by recursively traversing tree created by DTL, using item's attribute values to choose path
def classify(example, node, attr_dict):

    if node.isanswer:
        return node
    
    ex_val_in = attr_dict[node.attr][0]
    ex_val = example[0][ex_val_in]
    
    for child in node.children:
        if child.value == ex_val:
            return classify(example, child, attr_dict)
        
# Implementation of decision tree learning algorithm, with printing
def DTL(examples, attr_dict, parents, count, value):
    attributes = attr_dict.keys()
    
    # Case 1: If there are no more examples:
    if len(examples) == 0:
        
        classif = get_plurality(parents)[0]
        node = Node(classif, value, 0, 0, None, True)
        return node
        
    # Case 2: All examples have the same classification:
    # Number of examples with the dominant classification is the same as the number of examples.
    elif get_plurality(examples)[1] == len(examples):
        
        # We'll just take the classification of the first example because they're all the same.
        classif = examples[0][-1]
        if classif == 'yes':
            p = len(examples)
            n = 0
        else:
            p = 0
            n = len(examples)
        node = Node(classif, value, p, n, None, True)
        return node
        
    # Case 3: If the attributes list is empty:
    elif len(attributes) == 0:
        classif, count = get_plurality(examples)
        if classif == "yes":
            p = count
            n = len(examples)-count
        else:
            p = len(examples)-count
            n = count
        node = Node(classif, value, p, n, None, True)
        return node
    
    # Case 4: Recursive case. 
    else:
        attr = get_best_attr(attr_dict, examples)
        classif, count = get_plurality(examples)
        if classif == "yes":
            p = count
            n = len(examples)-count
        else:
            p = len(examples)-count
            n = count
        if p == 0 or n == 0:
            print "CHOICE NODE WITH p/n == 0!"
            print value + " : " + attr
        node = Node(None, value, p, n, attr, False)
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
            child = DTL(subexamples, subattr_dict, examples, count+1, val)
            node.children.append(child)

        return node

# Implement chi-sq pruning
def prune(node):
    
    if node.isanswer:
        return
    can_prune = True
    #observed = []
    #expected = []
    node_pos_float = float(node.pos)
    node_neg_float = float(node.neg)
    node_n = float(node.pos+node.neg)
    test_stat = 0.0
    for child in node.children:
        if not(child.isanswer):
            can_prune = False
            prune(child)
        else:
            obs_pos = float(child.pos)
            obs_neg = float(child.neg)
            #if obs_pos < 5 and obs_neg < 5:
                #can_prune = False
                #print "Less than 5"
            #else:
            if node_n == 0:
                print "node n is 0"
                print node.attr
                print child.classif
            expected_neg = node_neg_float*((obs_pos + obs_neg)/node_n)
            expected_pos = node_pos_float*((obs_pos + obs_neg)/node_n)
            # if obs_pos or obs_neg are zero, then we don't add anything
            if expected_neg == 0 or expected_pos == 0:
                print "expected 0"
                print expected_pos, expected_neg
                print obs_pos, obs_neg
                print node_pos_float, node_neg_float
                print node.attr
                print node.value
                print child.value
                print child.classif
            test_stat += math.pow((obs_pos-expected_pos), 2)/(expected_pos) 
            test_stat += math.pow((obs_neg-expected_neg), 2)/(expected_neg) 
                #observed.append(pos_float)
                #expected.append(node_pos_float*((pos_float + neg_float)/node_n))
    if (can_prune):
        #print "observed: ", observed
        #print "expected: ", expected
        
        df = len(node.children) - 1
        pval = 1 - scipy.stats.chi2.cdf(test_stat, df)
        if pval > 0.05:
            if node.pos > node.neg:
                node.classif = "yes"
            else:
                node.classif = "no"
            node.children = []
            node.attr = None
            node.isanswer = True
            
# The classification of a group of split examples.
class Node:
    def __init__(self, classif, value, pos, neg, attr, answer):
        self.classif = classif
        self.attr = attr
        self.value = value
        self.pos = pos
        self.neg = neg
        self.isanswer = answer
        self.children = []
        
    def __str__(self):
    	return self.classif
        

 	
def print_tree(node, count):
    if node.isanswer:
        print ": " + node.classif
    else:
        if count > 0:
            print
        for child in node.children:
            print count*'| ' + node.attr + " = " + child.value,
            print_tree(child, count+1)


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