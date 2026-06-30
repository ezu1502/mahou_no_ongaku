from rapidfuzz import process, fuzz

def get_matches (string, chosenlist, number_of_matches = 3):
    compared_string = string.lower()
    organized_list = []
    for indx, name in chosenlist:
        organized_list.append((indx, name))
        
    scores = [
    
    fuzz.partial_ratio(compared_string, chosenlist),
    2*fuzz.partial_token_sort_ratio(compared_string, chosenlist),
    fuzz.WRatio(compared_string, chosenlist),
    fuzz.partial_token_set_ratio(compared_string, chosenlist),
    fuzz.ratio(compared_string, chosenlist)

    ]

    finalscore = sum(scores)/len(scores) + 1
    otherlist = []
    for indx, name in chosenlist:
        otherlist.append(indx, name, finalscore)

    otherlist.sort(key=lambda item: item[2], reverse=True)
    otherlist = otherlist[:5]

    return otherlist
    
    #TODO CHECAR! NAO TERMINADO!
