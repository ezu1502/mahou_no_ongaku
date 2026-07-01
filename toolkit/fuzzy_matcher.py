from rapidfuzz import fuzz
import file_handler
def get_matches (string, chosenlist, number_of_matches = 3):
    compared_string = string.lower().strip()
        
    list_with_score = []
    for eachraw in chosenlist:
        if isinstance(eachraw, str):
            each = eachraw.lower().strip()
        elif isinstance(eachraw, tuple):
            name = eachraw[0]
            each = name.lower().strip()
        scores = [
        
        fuzz.partial_ratio(compared_string, each),
        2*fuzz.partial_token_sort_ratio(compared_string, each),
        fuzz.WRatio(compared_string, each),
        fuzz.partial_token_set_ratio(compared_string, each),
        fuzz.ratio(compared_string, each)

        ]
        
        finalscore = sum(scores)/6
        list_with_score.append((eachraw, finalscore))



    list_with_score.sort(key=lambda item: item[1], reverse=True)
    list_with_score = list_with_score[:number_of_matches]
    
    
    finallist = []
    
    for eachone in list_with_score:
        finallist.append(eachone[0])
        
    # file_handler.return_or_show_musiclist(finallist)



    return finallist
    
    #TODO CHECAR! NAO TERMINADO!


# for eachfile in files:
#         if eachfile.lower().endswith(".mp3"):
#             # eachfile_name = eachfile.replace("\ufeff", "")
#             music_files_list.append(eachfile)  

#     music_files_list.sort(key=lambda name: name.strip().lower())
#     return music_files_list

