'''
decisiontree.py
note that this will work even for non-binary classifications
'''
import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python decisiontree.py name_of_file.txt')
        sys.exit(1)
    
    else:
        f = open(sys.argv[1], 'r')
        text = f.readlines()
        
        # get the column headers, separate attributes from classification (last col)
        columns = text[0].strip('\n')
        splitted = columns.split('\t')
        classif = splitted[-1]
        attrs = splitted[0:-1]
        
        # store attributes in a dictionary: { attr_name : [column index, set(possible values)] }
        attr_dict = {}
        for i, a in enumerate(attrs):
            attr_dict[a] = [i, set([])]
        
        # parse each example into: [ [vals of each attribute], classification]
        data = text[1:]
        examples = []
        all_classifs = set([])
        
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
            all_classifs.add(ex_classif)

        node = DTL(examples, attr_dict, [], all_classifs, 0)
        print node
        
# Implementation of decision tree learning algorithm
def DTL(examples, attr_dict, parents, all_classifs, count):
    attributes = attr_dict.keys()
    
    # Case 1: If there are no more examples:
    if len(examples) == 0:
        
        classif = get_plurality(parents, all_classifs)[0]
        node = answer_node(classif)
        print ": " + classif
        return node
        
    # Case 2: All examples have the same classification:
    # Number of examples with the dominant classification is the same as the number of examples.
    elif get_plurality(examples, all_classifs)[1] == len(examples):
        
        # We'll just take the classification of the first example because they're all the same.
        classif = examples[1][-1]
        node = answer_node(classif)
        print ": " + classif
        return node
        
    # Case 3: If the attributes list is empty:
    elif len(attributes) == 0:
        classif = get_plurality(examples, all_classifs)[0]
        node = answer_node(classif)
        print ": " + classif
        return node
    
    # Case 4: Recursive case. 
    else:
        print
        attr = get_best_attr(attributes)
        node = choice_node(attr)
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
            print count*'| ' + str(attr) + " = " + str(val),
            child = DTL(subexamples, subattr_dict, examples, all_classifs, count+1)
            node.children.append(child)
        return node
        
# The classification of a group of split examples.
class answer_node:
    def __init__(self, classif):
        self.classif = classif
        
    def __str__(self):
    	print ": " + str(self.classif)

# The attribute split on and nodes resulting from the split.
class choice_node:
    def __init__(self, attr):
        self.attr = attr
        self.children = []
        
    def __str__(self):
    	print "--- choice node ---"
    	print self.attr
    	for child in self.children:
    	    print "*"
    	return "---"

'''    	
def print_tree(node):
    if class(node) == answer_node:
        print ": " + str(node.classif)
    else:
        print node.attr
''' 

# Get_plurality returns classification with highest percentage given example list and possible 
# classifications. It also returns how many examples had that classification.
def get_plurality(ex_list, classifs_set):
   
    count_dict = {}
    categories = list(classifs_set)
    for c in categories:
        count_dict[c] = 0
    
    for ex in ex_list:
        classif = ex[-1]
        count_dict[classif] += 1
    
    max = 0
    arg_max = categories[0]
    for c in categories:
        if (count_dict[c] > max):
            max = count_dict[c]
            arg_max = c
    return arg_max, max

def get_best_attr(attributes):
    return attributes[0]
    
    
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