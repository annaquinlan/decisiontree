'''
decisiontree.py
'''
import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python decisiontree.py name_of_file.txt')
        sys.exit(1)
    else:
        f = open(sys.argv[1], 'r')
        text = f.readlines()
        
        columns = text[0].strip('\n')
        splitted = columns.split('\t')
        classif = splitted[-1]
        attrs = splitted[0:-1]
        
        attr_dict = {}
        
        for i, a in enumerate(attrs):
            attr_dict[a] = [i, set([])]
        
        data = text[1:]
        examples = []
        all_classifs = set([])
        
        for line in data:
            cleanline = line.strip('\n')
            dataitems = cleanline.split('\t')
            
            chars = dataitems[0:-1]
            result = dataitems[-1]
            
            examples.append([chars, result])
            
            for i, a in enumerate(attrs):
                attr_dict[a][1].add(chars[i])
            all_classifs.add(result)

        DTL(examples, attr_dict, [], all_classifs)

# [
#    [ [attribute1, attribute2, ...], classification]
# ]
def DTL(examples, attr_dict, parents, all_classifs):
    attributes = attr_dict.keys()
    #if there are no more examples:
    #    make an answer node with plurality of parent examples
    #    return node
    if len(examples) == 0:
        classif = get_plurality(parents, all_classifs)[0]
        node = answer_node(classif)
        return node
        
    #elif if all examples have the same classification:
        #make answer node with that classification
        #return answer node
    elif get_plurality(examples, all_classifs)[1] == len(examples):
        classif = examples[1][-1]
        node = answer_node(classif)
        return node
        
    # elif if the attributes list is empty
    #    make an answer node with the plurality of the current examples
    #    return answer node
    elif len(attributes) == 0:
        classif = get_plurality(examples, all_classifs)[0]
        node = answer_node(classif)
        return node
    else:
        attr = get_best_attr(attributes)
        node = choice_node(attr)
        values = list(attr_dict[attr][1])
        index = attr_dict[attr][0]
        exsbyvals_dict = {}
        for val in values:
            exsbyvals_dict[val] = []
        
        for ex in examples:
            exval = ex[0][index]
            exsbyvals_dict[exval].append(ex)
        
        subattr_dict = dict(attr_dict)
        del subattr_dict[attr]
        for val in values:
            subexamples = exsbyvals_dict[val]
            child = DTL(subexamples, subattr_dict, examples, all_classifs)
            node.children.append(child)
        return node
        
        
class answer_node:
    def __init__(self, classif):
        self.classif = classif
    
class choice_node:
    def __init__(self, attr):
        self.attr = attr
        self.children = []
        
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