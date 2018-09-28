import numpy

def min_el(a, b, c):
    if a <= b and a <= c:
        return 1, a
    elif b <= c and b <= a:
        return 2, b
    else:
        return 3, c

def find_spell_errors(word_ref, word_error):
    """
    return all variants of substitutions, insertions, deletions in an incorrect word
    """
    n = len(word_ref)
    d = numpy.zeros((len(word_ref)+1)*(len(word_error)+1))
    d = d.reshape((len(word_ref)+1, len(word_error)+1))
    
    variants = []
    path = numpy.zeros((len(word_ref)+1)*(len(word_error)+1))
    path = path.reshape((len(word_ref)+1, len(word_error)+1))

    for i in range(len(word_ref)+1):
        for j in range(len(word_error)+1):
            if i == 0:
                d[0][j] = j
                path[0][j] = 2
            elif j == 0:
                d[i][0] = i 
                path[i][0] = 3
    
    path[0][0] = 0
    variants.append(path)
    
    for i in range(1, len(word_ref)+1):
        for j in range(1, len(word_error)+1):
            if word_ref[i-1] == word_error[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                sub = d[i-1][j-1] + 1
                ins = d[i][j-1] + 1
                de = d[i-1][j] + 1
                path[i][j], d[i][j] = min_el(sub, ins, de)

    i = len(word_ref); j = len(word_error)
    
    substitution = {}
    insertion = {}
    deletion = {}
    
    t_del = ""; t_ins = ""
    
    while i != 0 or j != 0:
        if path[i][j] == 1:
            sub = (word_ref[i - 1], word_error[j - 1])
            if sub not in substitution.keys():
                substitution[sub] = 0
            substitution[sub] += 1
            i -= 1
            j -= 1
        elif path[i][j] == 2:
            t_ins += word_error[j - 1]
            if path[i][j - 1] != 2:
                if j > 1:
                    t_ins += word_error[j - 2]
                if i == 0:
                    ins = ("#", t_ins[::-1])
                else:
                    ins = (word_ref[i - 1], t_ins[::-1])
                    
                if ins not in insertion.keys():
                    insertion[ins] = 0
                insertion[ins] += 1
                t_ins = ""
                
                if j != 1:
                    j -= 1
                if i != 0:
                    i -= 1
            j -= 1
        elif path[i][j] == 3:
            t_del += word_ref[i - 1]
            if path[i - 1][j] != 3:
                if i > 1:
                    t_del += word_ref[i - 2]
                if j == 0:
                    dl = (t_del[::-1], "#")
                else:
                    dl = (t_del[::-1], word_error[j - 1]) 
                    
                if dl not in deletion.keys():
                    deletion[dl] = 0
                deletion[dl] += 1
                t_del = ""
                
                if j != 0:
                    j -= 1
                if i != 1:
                    i -= 1
            i -= 1
        else:
            i -= 1
            j -= 1

    return substitution, insertion, deletion