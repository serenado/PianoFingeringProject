def split(part):
    '''
    Split a given piano part (for a single hand) into ascending and descending chunks.
    Returns a list of [INSERT DATA STRUCTURE] each representing a monotonic chunk of notes.
    Adjacent chunks share a note.
    
    As an example, Mary Had a Little Lamb would be split like so:
        input: EDCDEEEDDDEGGEDCDEEEEDDDEDC
        output: EDC, CDEEE, EDDD, DEGG, GEDC, CDEEEE, EDDD, DE, EDC
        
    TODO: long enough rests should signify a break where the hand can be reset to any finger
    '''
    return [part]

def finger(score):
    '''
    Given a piano score, produce a reasonable fingering.
    '''
    return score