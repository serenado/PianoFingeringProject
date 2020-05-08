import monotonic
from music21 import *

def split(part):
    '''
    Split a given piano part (for a single hand) into ascending and descending chunks.
    Returns a list of lists each representing a monotonic chunk of notes.
    Adjacent chunks share a note.
    
    As an example, Mary Had a Little Lamb would be split like so:
        input: EDCDEEEDDDEGGEDCDEEEEDDDEDC
        output: EDC, CDEEE, EDDD, DEGG, GEDC, CDEEEE, EDDD, DE, EDC
        
    TODO: long enough rests should signify a break where the hand can be reset to any finger
    '''
    chunks = []
    current_chunk = [part.flat.notes[0], part.flat.notes[1]]
    is_ascending = current_chunk[1].pitch.ps >= current_chunk[1].pitch.ps           # true if the 2nd note is weakly higher than 1st note

    for i in range(2, len(part.flat.notes)):
        prev_note = current_chunk[-1]
        current_note = part.flat.notes[i]
        if is_ascending:
            if current_note.pitch.ps >= prev_note.pitch.ps:
                current_chunk.append(current_note)
            else:
                # switch to descending now                               
                chunks.append(current_chunk)
                current_chunk = [prev_note, current_note]
                is_ascending = False
        else:
            if current_note.pitch.ps <= prev_note.pitch.ps:
                current_chunk.append(current_note)
            else:
                # switch to ascending now
                chunks.append(current_chunk)
                current_chunk = [prev_note, current_note]
                is_ascending = True
    chunks.append(current_chunk)
    return chunks

def finger(score):
    '''
    Given a right-hand piano score, returns a score with an annotated fingering.
    '''    
    chunks = split(score)

    # keep memo tables to avoid repeat calculations
    memo_table = dict() 
    transition_table = dict()

    best_score = 0
    best_fingering = []

    # try ending on every finger
    for j in range(1, 6):
        fingering, points = compute_best_score(chunks, len(chunks) - 1, j, memo_table, transition_table)
        if points > best_score:
            best_score = points
            best_fingering = fingering

    annotated_score = monotonic.annotate_score(score, best_fingering)

    print( best_score / (len(chunks) * 10))
    return annotated_score


def compute_best_score(chunks, i, j, memo_table, transition_table):
    '''
    Computes best score for all chunks up to chunks[i] where chunk i ends with finger j
    Returns (fingering, total score)
    '''
    possible_fingers = [1,2,3,4,5]

    # store TransitionScores to avoid calling finger_monotonic multiple times
    if i in transition_table:
        transition_score = transition_table[i]
    else:
        transition_score = TransitionScores(chunks[i])
        transition_table[i] = transition_score

    # base case
    if i == 0:
        # find best starting finger
        best_start = max(possible_fingers, key=lambda start: transition_score.get_fingering_option(start, j)[1])
        fingering, score = transition_score.get_fingering_option( best_start, j)
        memo_table[(i, j)] = fingering, score
        return (fingering, score)

    score = 0
    fingering = []
    # try every possible end finger for this chunk
    for e in possible_fingers:
        # see if subproblem is in memo_table
        if (i-1, e) in memo_table:
            prev_fingering, prev_score = memo_table[(i-1, e)]
        else:
            prev_fingering, prev_score = compute_best_score(chunks, i-1, e, memo_table, transition_table)
        possible_fingering, possible_score = transition_score.get_fingering_option(e, j)

        # if this new fingering works, update
        if possible_fingering != [] and prev_score + possible_score > score:
            score = prev_score + possible_score
            fingering = prev_fingering + possible_fingering[1:]
    #store in table
    memo_table[(i, j)] = fingering, score
    return (fingering, score)

class TransitionScores:
    def __init__(self,  chunk):
        self.chunk = chunk
        self.fingerings = monotonic.finger_monotonic(self.chunk)

    def get_fingering_option(self, start_finger, end_finger):
        '''
        Gets the best fingering that starts on start_finger
        and ends on end_finger.
        Returns (fingering, score). If not found, returns ([], 0)
        '''
        for fingering, score in self.fingerings:
            if fingering[0] == start_finger and fingering[-1] == end_finger:
                return (fingering, score)

        return ([], 0)


################################################################################
#                                                                              #
#                                   TESTS                                      #
#                                                                              #
################################################################################

def test_c_maj_scale():
    c_maj_scale = converter.parse('./data/scales/cmaj.mxl')
    result = finger(c_maj_scale.parts[0])
    result.show()

def test_b_maj_scale():
    b_maj_scale = converter.parse('./data/scales/bmaj.mxl')
    result = finger(b_maj_scale.parts[0])
    result.show()

def test_c_maj_arpeggio():
    c_maj_arpeggio = converter.parse('./data/arpeggios/cmaj.mxl')
    result = finger(c_maj_arpeggio.parts[0])
    result.show()

def test_bwv108_soprano():
    bach = corpus.parse('bach/bwv108.6.xml')
    result = finger(bach.parts[0])
    result.show()


# test_c_maj_scale()
# test_c_maj_arpeggio()
# test_c_maj_arpeggio()
test_bwv108_soprano()



