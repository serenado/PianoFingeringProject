import monotonic
import copy
from music21 import *

def split(part, rh=True, rest_flag=-1):
    '''
    Split a given piano part (for a single hand) into ascending and descending chunks.
    Returns a list of lists each representing a monotonic chunk of notes.
    Adjacent chunks share a note.

    rest_flag is used to decide which (if any) rests should be used as moments to split into a chunk.
    If rest_flag is -1, rests will not be used as rests.
    If rest_flag > 0, rest_flag represents the number of quarter notes necessary for a rest to be
    used as a reset.
    
    As an example, Mary Had a Little Lamb would be split like so:
        input: EDCDEEEDDDEGGEDCDEEEEDDDEDC
        output: EDC, CDEEE, EDDD, DEGG, GEDC, CDEEEE, EDDD, DE, EDC

    Currently, our algorithm is not able to provide fingering for chords. If the part contains
    chords, they will be replaced by a single note from that chord. If rh is True, we choose
    the top note. Otherwise, we choose the bottom note.
    
    '''
    chunks = []
    note_1 = part.flat.notes[0]
    if isinstance(note_1, chord.Chord):
        if rh:
            note_w = note_w.notes[-1] # set current note to highest note in chord
        else:
            note_w = note_w.notes[0] # set current note to lowest note in chord
    note_2 = part.flat.notes[1]
    if isinstance(note_2, chord.Chord):
        if rh:
            note_2 = note_2.notes[-1] # set current note to highest note in chord
        else:
            note_2 = note_2.notes[0] # set current note to lowest note in chord
    current_chunk = [note_1, note_2]
    is_ascending = current_chunk[1].pitch.ps >= current_chunk[0].pitch.ps           # true if the 2nd note is weakly higher than 1st note

    for i in range(2, len(part.flat.notesAndRests)):
        prev_note = current_chunk[-1]
        current_note = part.flat.notesAndRests[i]

        if isinstance(current_note, note.Rest):     
            if i == len(part.flat.notesAndRests)-1:         # if part ends on rest
                break

            if rest_flag != -1 and current_note.duration.quarterLength >= rest_flag:
                if len(current_chunk) != 1:
                    chunks.append(current_chunk)

                current_chunk = [prev_note]
                # Assumes ascending, changes later if this guess is wrong
                is_ascending = True        
            continue


        elif isinstance(current_note, chord.Chord):
            if rh:
                current_note = current_note.notes[-1] # set current note to highest note in chord
            else:
                current_note = current_note.notes[0] # set current note to lowest note in chord
        if is_ascending:
            if current_note.pitch.ps >= prev_note.pitch.ps:
                current_chunk.append(current_note)
            elif len(current_chunk) == 1:
                # if we just left a chord and guessed incorrectly
                current_chunk.append(current_note)
                is_ascending = False
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

def finger_both(score, rest_flag=-1):
    '''
    Given a piano score, returns a score with annotated fingerings for both hands.
    '''
    annotated_rh = finger(score.parts[0], rest_flag=rest_flag)
    annotated_lh = finger(score.parts[1], False, rest_flag=rest_flag)

    annotated_score = copy.deepcopy(score)

    return annotated_score

def finger(score, rh=True, rest_flag=-1):
    '''
    Given a single-hand piano score, returns a score with an annotated fingering. If rh is True, generate
    a right-handed fingering. Otherwise, generate a left-handed fingering.
    '''    
    chunks = split(score, rh, rest_flag=rest_flag)

    # keep memo tables to avoid repeat calculations
    memo_table = dict() 
    transition_table = dict()

    best_score = 0
    best_fingering = []

    # try ending on every finger
    for j in range(1, 6):
        fingering, points = compute_best_score(chunks, len(chunks) - 1, j, memo_table, transition_table, rh)
        if points > best_score:
            best_score = points
            best_fingering = fingering

    annotated_score = monotonic.annotate_score(score, best_fingering, rh=rh)

    print( best_score / (len(chunks) * 10))
    return annotated_score


def compute_best_score(chunks, i, j, memo_table, transition_table, rh=True):
    '''
    Computes best score for all chunks up to chunks[i] where chunk i ends with finger j
    Returns (fingering, total score)
    '''
    possible_fingers = [1,2,3,4,5]

    # store TransitionScores to avoid calling finger_monotonic multiple times
    if i in transition_table:
        transition_score = transition_table[i]
    else:
        transition_score = TransitionScores(chunks[i], rh)
        transition_table[i] = transition_score

    # base case
    if i == 0:
        # find best starting finger
        best_start = max(possible_fingers, key=lambda start: transition_score.get_fingering_option(start, j)[1])
        fingering, score = transition_score.get_fingering_option(best_start, j)
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
            prev_fingering, prev_score = compute_best_score(chunks, i-1, e, memo_table, transition_table, rh)
        possible_fingering, possible_score = transition_score.get_fingering_option(e, j)

        # if this new fingering works, update
        if possible_fingering != [] and prev_score + possible_score > score:
            score = prev_score + possible_score
            fingering = prev_fingering + possible_fingering[1:]
    #store in table
    memo_table[(i, j)] = fingering, score
    return (fingering, score)

class TransitionScores:
    def __init__(self,  chunk, rh=True):
        self.chunk = chunk
        self.fingerings = monotonic.finger_monotonic(self.chunk, rh)

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

def test_k545():
    k545 = corpus.parse('mozart/k545')
    result = finger_both(k545)
    result.show()

def test_k545_with_split():
    k545 = corpus.parse('mozart/k545')
    result = finger_both(k545,rest_flag=1.0)
    result.show()


# test_c_maj_scale()
# test_c_maj_arpeggio()
# test_c_maj_arpeggio()
# test_bwv108_soprano()
# test_k545()
# test_k545_with_split()
