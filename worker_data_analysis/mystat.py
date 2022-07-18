import math

def KM(s, z):
    su = 1;
    nom = 1;
    denom = 1;
    log_nom = math.log(nom);
    log_denom = math.log(denom);
    log_s = math.log(s);
    log_z = math.log(z);
    for i in range(1000):
        log_nom += log_z;
        s += 1;
        log_s = math.log(s);
        log_denom += log_s;
        log_sum = log_nom - log_denom;
        su += math.exp(log_sum);
    return su;

def log_igf(s, z):
        if z <= 0:
            return 0
        sc = (math.log(z) * s) - z - math.log(s);
        k = KM(s, z);
        return math.log(k) + sc;

def getApproxGamma(n):
        return math.pow((1 / ((12 * n) - 1 / (10 * n)) + n) / math.e, n) * math.sqrt(2 * math.pi / n)

def ChiSquare2pValue(df, x2):
        if x2 < 0 or df < 1:
            return 0.0
        k = df * 0.5
        v = x2 * 0.5
        if df == 2:
            return math.exp(-1.0 * v)
        incompleteGamma = log_igf(k,v)
        gamma = math.log(getApproxGamma(k))
        incompleteGamma -= gamma
        if(math.exp(incompleteGamma) > 1):
            return 1e-14
        pValue = 1.0 - math.exp(incompleteGamma)
        return pValue

def ChiSquareTest(matrix):
    rowsum = [sum(row) for row in matrix]
    colsum = [sum(col) for col in zip(*matrix)]
    expected = [element / sum(rowsum) for element in rowsum]
    x2 = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if expected[i] * colsum[j] == 0:
                continue;
            x2 += (expected[i] * colsum[j] - matrix[i][j])**2 / (expected[i] * colsum[j])
    df = (len(matrix) - 1) * (len(matrix[0]) - 1)

    return df, x2, ChiSquare2pValue(df, x2)