import constants
import monotonic # just for annotate_score
import copy
from music21 import *

'''
Don't use chunks.
'''

def get_transitions(part, rh=True, rest_flag=-1):
    '''
    Transform a given piano part (for a single hand) into list of Transitions.
    Returns a list of Transition objects each representing a transition between two notes.
    Adjacent Transitions share a note.

    rest_flag is used to decide which (if any) rests should be used as moments to reset the hand.
    If rest_flag is -1, rests will not be used as resets.
    If rest_flag > 0, rest_flag represents the number of quarter notes necessary for a rest to be
    used as a reset.

    Currently, our algorithm is not able to provide fingering for chords. If the part contains
    chords, they will be replaced by a single note from that chord. If rh is True, we choose
    the top note. Otherwise, we choose the bottom note.
    '''
    transitions = []

    notes_and_rests = list(part.flat.notesAndRests)

    # find index of first real note
    first_note_index = 0
    while(first_note_index < len(notes_and_rests) and isinstance(notes_and_rests[first_note_index], note.Rest)):
        first_note_index += 1

    # initialize first note, handle case where it is a chord
    note_1 = notes_and_rests[first_note_index]
    if isinstance(note_1, chord.Chord):
        if rh:
            note_1 = note_1.notes[-1] # set current note to highest note in chord
        else:
            note_1 = note_1.notes[0] # set current note to lowest note in chord

    # iterate through remaining notes and create Transitions
    rest_duration = 0 # used to remember how long of a rest is between notes
    for i in range(1 + first_note_index, len(notes_and_rests)):
        note_2 = notes_and_rests[i]

        # if it's a chord, replace with a single note
        if isinstance(note_2, chord.Chord):
            if rh:
                note_2 = note_2.notes[-1] # set current note to highest note in chord
            else:
                note_2 = note_2.notes[0] # set current note to lowest note in chord
        
        # if it's a rest, update rest_duration
        if isinstance(note_2, note.Rest):     
            rest_duration += note_2.duration.quarterLength

        # otherwise, add a new Transition
        else:
            can_reset = rest_flag != -1 and rest_duration >= rest_flag
            transitions.append(Transition(note_1, note_2, rh, can_reset))
            # update variables
            note_1 = note_2
            rest_duration = 0

    return transitions

def finger(score, rh=True, rest_flag=-1):
    '''
    Given a single-hand piano score, returns a score with an annotated fingering. If rh is True, generate
    a right-handed fingering. Otherwise, generate a left-handed fingering.
    '''    
    transitions = get_transitions(score, rh, rest_flag=rest_flag)

    # keep memo tables to avoid repeat calculations
    memo_table = dict() 

    best_score = 0
    best_fingering = []

    # try ending on every finger
    for j in [1, 2, 3, 4, 5]:
        fingering, comfort_score = compute_best_comfort_score(transitions, len(transitions) - 1, j, memo_table, rh)
        if comfort_score > best_score:
            best_score = comfort_score
            best_fingering = fingering + [j]

    annotated_score = monotonic.annotate_score(score, best_fingering, rh=rh)

    print(best_fingering)
    print(best_score / (len(transitions) * 10))
    return annotated_score


def compute_best_comfort_score(transitions, i, j, memo_table, rh=True):
    '''
    Computes best score for all transitions up to transitions[i] where transition i ends with finger j
    Returns (fingering, total score)

    TODO: incorporate hand resets on long rests
    '''
    possible_fingers = [1, 2, 3, 4, 5]

    transition = transitions[i]

    # base case
    if i == 0:
        # find best starting finger
        best_start = max(possible_fingers, key=lambda start: transition.finger_pairs.get((start, j), 0))
        score = transition.finger_pairs.get((best_start, j), -1)
        memo_table[(i, j)] = [best_start], score
        return ([best_start], score)

    score = 0
    fingering = []
    # try every possible start finger for this transition
    for f in possible_fingers:
        # see if subproblem is in memo_table
        if (i-1, f) in memo_table:
            prev_fingering, prev_score = memo_table[(i-1, f)]
        else:
            prev_fingering, prev_score = compute_best_comfort_score(transitions, i-1, f, memo_table, rh)
        possible_score = transition.finger_pairs.get((f, j), -1)

        # update
        if possible_score != -1 and prev_score + possible_score > score:
            score = prev_score + possible_score
            fingering = prev_fingering + [f]

    # store in table
    memo_table[(i, j)] = fingering, score
    return (fingering, score)

def finger_both(score, rest_flag=-1):
    '''
    Given a piano score, returns a score with annotated fingerings for both hands.
    '''
    annotated_rh = finger(score.parts[0], rest_flag=rest_flag)
    annotated_lh = finger(score.parts[1], False, rest_flag=rest_flag)

    annotated_score = copy.deepcopy(score)

    return annotated_score

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

class Transition:
    def __init__(self, note_1, note_2, rh=True, can_reset=False):
        self.note_1 = note_1
        self.note_2 = note_2
        self.rh = rh
        self.can_reset = can_reset
        self.finger_pairs = self.get_finger_pairs()

    def __repr__(self):
        if self.can_reset:
            arrow = ' ~~~> '
        else:
            arrow = ' ---> '
        return self.note_1.nameWithOctave + arrow + self.note_2.nameWithOctave + ' : ' + str(self.finger_pairs) + '\n'

    def get_finger_pairs(self):
        distance = max(min(self.note_2.pitch.ps - self.note_1.pitch.ps, 13), -13) # CLAMP DOWN TO 13
        prev_color = monotonic.get_color(self.note_1)
        color = monotonic.get_color(self.note_2)

        # get valid finger pairs from the comfort score table
        if self.rh:
            if distance >= 0:
                finger_pairs = constants.COMFORT[(distance, prev_color, color)]
            else:
                finger_pairs = constants.COMFORT[(-distance, color, prev_color)]
        else:
            if distance >= 0:
                finger_pairs = constants.COMFORT[(distance, color, prev_color)]
            else:
                finger_pairs = constants.COMFORT[(-distance, prev_color, color)]

        # switch order of fingers if necessary
        if (self.rh and distance < 0) or (not self.rh and distance >= 0):
            finger_pairs = { (fingers[1], fingers[0]) : finger_pairs[fingers] for fingers in finger_pairs }

        return finger_pairs

################################################################################
#                                                                              #
#                                   TESTS                                      #
#                                                                              #
################################################################################

def test_get_transitions():
    b_maj_scale = converter.parse('./data/scales/bmaj.mxl')
    result = get_transitions(b_maj_scale.parts[0])
    print(result)

def test_get_transitions_k545():
    k545 = corpus.parse('mozart/k545')
    result = get_transitions(k545.parts[0], True, 1)
    print(result)

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

# test_get_transitions()
# test_get_transitions_k545()

test_c_maj_scale()
# test_b_maj_scale()
# test_c_maj_arpeggio()
# test_bwv108_soprano()
# test_k545()
# test_k545_with_split()




