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
        for a in attrs:
            attr_dict[a] = set([])
        
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
                attr_dict[a].add(chars[i])
            all_classifs.add(result)

        print attr_dict


    
    
if __name__ == "__main__":
    main()