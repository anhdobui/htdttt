def checkIsImperative(doc, score):
    verb_position = []
    obj_position = []
    
    for i, token in enumerate(doc):
        if "ROOT" in token.dep_:
            verb_position.append(i)
            score += 1
        elif "obj" in token.dep_:
            obj_position.append(i)
    if(len(verb_position) == 0 or len(obj_position) == 0):
        return score
    if(len(verb_position) > 1 or len(obj_position) > 1):
        return -1
    if(verb_position[0] == 0):
        return 10
    return score


def checkIsInterrogative(doc, score):
    aux_position = []
    wh_position = []
    subj_position = []
    verb_position = []

    for i, token in enumerate(doc):
        print(token, token.dep_)
        if token.text.lower() in ["who", "what", "where", "how", "why"]:
            wh_position.append(i)
            score += 1
        elif "aux" in token.dep_:
            aux_position.append(i)
            score += 1
        elif "nsubj" in token.dep_:
            subj_position.append(i)
            score += 1
        elif "ROOT" in token.dep_:
            verb_position.append(i)
            score += 1
    if(len(verb_position) == 0 or len(wh_position) == 0 or len(aux_position or len(subj_position)) == 0):
        return score
    if(len(aux_position) > 1 or len(wh_position) > 1 or len(subj_position) > 1 or len(verb_position) > 1):
        return -1
    if(len(wh_position) == 1 and wh_position[0] < aux_position[0] < subj_position[0] < verb_position[0]):
        score = 10
    if(len(wh_position) == 0 and aux_position[0] < subj_position[0] < verb_position[0]):
        score = 10
    return score

def checkIsDeclarative(doc, score):
    subj_position = []
    verb_position = []
    obj_position = []

    for i, token in enumerate(doc):
        print(token, token.dep_)
        if "nsubj" in token.dep_:
            subj_position.append(i)
            score += 1
        elif "ROOT" in token.dep_:
            verb_position.append(i)
            score += 1
        elif "obj" in token.dep_:
            obj_position.append(i)
            score += 1
    if(len(subj_position) == 0 or len(verb_position) == 0 or len(obj_position) == 0):
        return score
    if len(subj_position) > 1 or len(verb_position) > 1 or len(obj_position) > 1:
        return -1
    if subj_position[0] < verb_position[0] < obj_position[0]:
        score = 10
    return score