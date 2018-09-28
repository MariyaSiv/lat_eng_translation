import numpy


def min_el(a, b, c):
    if a <= b and a <= c:
        return 1, a
    elif b <= c and b <= a:
        return 2, b
    else:
        return 3, c


def WER(text_OCR, text_reference):
    """WER = (iw + sw + dw) / nw where nw is the number of words, sw is the number of words substituted, dw the number of words deleted and i the number of words inserted (among all possible transformations, that one minimizing the sum iw + sw + dw is chosen)"""
    text_OCR = numpy.array(text_OCR)
    text_reference = numpy.array(text_reference)

    n = len(text_reference)

    d = numpy.zeros((len(text_reference)+1)*(len(text_OCR)+1))
    d = d.reshape((len(text_reference)+1, len(text_OCR)+1))

    path = numpy.zeros((len(text_reference)+1)*(len(text_OCR)+1))
    path = path.reshape((len(text_reference)+1, len(text_OCR)+1))

    for i in range(len(text_reference)+1):
        for j in range(len(text_OCR)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(text_reference)+1):
        for j in range(1, len(text_OCR)+1):
            if text_reference[i-1] == text_OCR[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                sub = d[i-1][j-1] + 1
                ins = d[i][j-1] + 1
                de = d[i-1][j] + 1
                path[i][j], d[i][j] = min_el(sub, ins, de)

    i = len(text_reference)
    j = len(text_OCR)

    substition = 0
    insertion = 0
    deletion = 0

    while i != 0 and j != 0:
        if path[i][j] == 1:
            substition += 1
            i -= 1
            j -= 1
        elif path[i][j] == 2:
            insertion += 1
            j -= 1
        elif path[i][j] == 3:
            deletion += 1
            i -= 1
        else:
            i -= 1
            j -= 1

    results = [substition, insertion, deletion]
    return results, d[len(text_reference)][len(text_OCR)] / n


def CER(text_OCR, text_reference):
    """using the total number n of characters and the minimal number of character insertions i, substitutions s an deletions d required to transform the reference text into the OCR output."""
    
    text_OCR = ' '.join(text_OCR)
    text_reference = ' '.join(text_reference)

    text_OCR = numpy.array(list(text_OCR))
    text_reference = numpy.array(list(text_reference))

    n = len(text_reference)

    d = numpy.zeros((len(text_reference)+1)*(len(text_OCR)+1))
    d = d.reshape((len(text_reference)+1, len(text_OCR)+1))
    path = numpy.zeros((len(text_reference)+1)*(len(text_OCR)+1))
    path = path.reshape((len(text_reference)+1, len(text_OCR)+1))

    for i in range(len(text_reference)+1):
        for j in range(len(text_OCR)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(text_reference)+1):
        for j in range(1, len(text_OCR)+1):
            if text_reference[i-1] == text_OCR[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                s = d[i-1][j-1] + 1
                ins = d[i][j-1] + 1
                de = d[i-1][j] + 1
                path[i][j], d[i][j] = min_el(s, ins, de)

    i = len(text_reference)
    j = len(text_OCR)

    substition = 0
    insertion = 0
    deletion = 0

    while i != 0 and j != 0:
        if path[i][j] == 1:
            substition += 1
            i -= 1
            j -= 1
        elif path[i][j] == 2:
            insertion += 1
            j -= 1
        elif path[i][j] == 3:
            deletion += 1
            i -= 1
        else:
            i -= 1
            j -= 1

    results = [substition, insertion, deletion]
    return results, d[len(text_reference)][len(text_OCR)] / n
