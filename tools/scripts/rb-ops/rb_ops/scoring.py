"""Existing CVSS v3.1 base scoring and strict edit-vector parsing."""
AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
AC = {"L": 0.77, "H": 0.44}
PR_U = {"N": 0.85, "L": 0.62, "H": 0.27}
PR_C = {"N": 0.85, "L": 0.68, "H": 0.5}
UI = {"N": 0.85, "R": 0.62}
CIA = {"H": 0.56, "L": 0.22, "N": 0.0}
SEVERITY = [(0.0, "None"), (0.1, "Low"), (4.0, "Medium"), (7.0, "High"), (9.0, "Critical")]


def roundup_1(x: float) -> float:
    import math
    return math.ceil(x * 10) / 10.0


def cvss_base_score(vector: dict[str, str]) -> float:
    import math
    iss = 1 - ((1 - CIA[vector['C']]) * (1 - CIA[vector['I']]) * (1 - CIA[vector['A']]))
    if vector['S'] == 'U':
        impact = 6.42 * iss
        pr = PR_U[vector['PR']]
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)
        pr = PR_C[vector['PR']]
    exploitability = 8.22 * AV[vector['AV']] * AC[vector['AC']] * pr * UI[vector['UI']]
    if impact <= 0:
        return 0.0
    if vector['S'] == 'U':
        score = min(impact + exploitability, 10)
    else:
        score = min(1.08 * (impact + exploitability), 10)
    return roundup_1(score)


def severity_label(score: float) -> str:
    if score == 0.0:
        return "None"
    if score >= 9.0:
        return "Critical"
    if score >= 7.0:
        return "High"
    if score >= 4.0:
        return "Medium"
    return "Low"



def parse_vector(value):
    parts = value.split('/')
    if parts[0] != 'CVSS:3.1':
        raise ValueError('Only complete CVSS:3.1 base vectors are supported.')
    allowed = {'AV': 'NALP', 'AC': 'LH', 'PR': 'NLH', 'UI': 'NR', 'S': 'UC',
               'C': 'HLN', 'I': 'HLN', 'A': 'HLN'}
    vector = {}
    for part in parts[1:]:
        pair = part.split(':')
        if len(pair) != 2 or pair[0] not in allowed or pair[0] in vector or pair[1] not in tuple(allowed[pair[0]]):
            raise ValueError('Invalid or duplicate CVSS base metric.')
        vector[pair[0]] = pair[1]
    if set(vector) != set(allowed):
        raise ValueError('All eight CVSS base metrics are required.')
    canonical = 'CVSS:3.1/' + '/'.join(f'{key}:{vector[key]}' for key in allowed)
    score = cvss_base_score(vector)
    return canonical, score, severity_label(score)
