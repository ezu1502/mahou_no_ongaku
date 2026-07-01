#Meus atalhos de matemática

def mean(*args):
    total = 0
    length = len(args)
    if length > 0:
        total = sum(args)
        return total/length
    return None
   
    
