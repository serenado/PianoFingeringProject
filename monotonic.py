from music21 import *
import constants
import copy

'''
TODO: introduce pruning to only keep best fingerings?
TODO: favor fingerings that start on 1, end on 5 for ascending, start on 5, end on 1 for descending?
TODO: may need a better way of associating fingers to notes
'''
def finger_monotonic(notes, rh=True):
	'''
	Given a monotonic list of notes (either ascending or descending), produces a list of
	potential fingerings, with a comfort score for each.
	
	TODO: what data structure?
	'''
	fingerings = [([1], 0), ([2], 0), ([3], 0), ([4], 0), ([5], 0)]
	prev_note = notes[0]
	prev_color = get_color(prev_note)
	for note in notes[1:]:
		new_fingerings = []

		distance = max(min(note.pitch.ps - prev_note.pitch.ps, 13), -13) # CLAMP DOWN TO 13
		color = get_color(note)
		if rh:
			if distance >= 0:
				finger_pairs = constants.COMFORT[(distance, prev_color, color)]
			else:
				finger_pairs = constants.COMFORT[(-distance, color, prev_color)]
		else:
			if distance >= 0:
				finger_pairs = constants.COMFORT[(distance, color, prev_color)]
			else:
				finger_pairs = constants.COMFORT[(-distance, prev_color, color)]

		# for each partial fingering, try possible next fingers
		for fingering, score in fingerings:
			prev_finger = fingering[-1]
			for finger in [1, 2, 3, 4, 5]:
				if (rh and distance >= 0) or (not rh and distance < 0):
					finger_pair = (prev_finger, finger)
				else:
					finger_pair = (finger, prev_finger)
				if finger_pair in finger_pairs:
					comfort_score = finger_pairs[finger_pair]
					new_fingerings.append((fingering + [finger], score + comfort_score))

		fingerings = new_fingerings
		prev_note = note
		prev_color = color
	
	fingerings = [(f[0], f[1] / (len(notes) - 1)) for f in fingerings]
	return sorted(fingerings, key=lambda f: f[1], reverse=True)

def get_color(note):
	if note.pitch.pitchClass in [0, 2, 4, 5, 7, 9, 11]:
		return 'white'
	return 'black'

def annotate_score(score, fingering, offset=0, rh=True):
	'''
	Makes a new score by adding fingering numbers according to a array of fingerings.
	If offset if specified, starts adding fingering after offset number of notes
	from the beginning of the score.

	Replaces chords with a single note. If rh is True, chooses the top note. Otherwise,
	chooses the bottom note.
	'''
	new_score = copy.deepcopy(score)
	for i in range(len(fingering)):
		if isinstance(score.flat.notes[i+offset], chord.Chord):
			if rh:
				index = -1
			else:
				index = 0
			score.flat.notes[i+offset].activeSite.replace(score.flat.notes[i+offset], score.flat.notes[i+offset].notes[index])
		score.flat.notes[i+offset].articulations.append(articulations.Fingering(fingering[i]))
	return score

################################################################################
#																			   #
#									TESTS 									   #
#																			   #
################################################################################

def test_c_maj_scale_up():
	c_maj_scale = converter.parse('./data/scales/cmaj.mxl')
	fingerings = finger_monotonic(c_maj_scale.parts[0].flat.notes[:15])
	print(len(fingerings))
	print(fingerings[:3])

def test_b_maj_scale_up():
	b_maj_scale = converter.parse('./data/scales/bmaj.mxl')
	fingerings = finger_monotonic(b_maj_scale.parts[0].flat.notes[:15])
	print(len(fingerings))
	print(fingerings[:3])

def test_f_maj_scale_up():
	f_maj_scale = converter.parse('./data/scales/fmaj.mxl')
	fingerings = finger_monotonic(f_maj_scale.parts[0].flat.notes[:15])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_sharp_maj_scale_up():
	c_sharp_maj_scale = converter.parse('./data/scales/csharpmaj.mxl')
	fingerings = finger_monotonic(c_sharp_maj_scale.parts[0].flat.notes[:15])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_maj_scale_up_lh():
	c_maj_scale = converter.parse('./data/scales/cmaj.mxl')
	fingerings = finger_monotonic(c_maj_scale.parts[1].flat.notes[:15], False)
	print(len(fingerings))
	print(fingerings[:3])

def test_b_maj_scale_up_lh():
	b_maj_scale = converter.parse('./data/scales/bmaj.mxl')
	fingerings = finger_monotonic(b_maj_scale.parts[1].flat.notes[:15], False)
	print(len(fingerings))
	print(fingerings[:3])

def test_f_maj_scale_up_lh():
	f_maj_scale = converter.parse('./data/scales/fmaj.mxl')
	fingerings = finger_monotonic(f_maj_scale.parts[1].flat.notes[:15], False)
	print(len(fingerings))
	print(fingerings[:3])

def test_c_sharp_maj_scale_up_lh():
	c_sharp_maj_scale = converter.parse('./data/scales/csharpmaj.mxl')
	fingerings = finger_monotonic(c_sharp_maj_scale.parts[1].flat.notes[:15], False)
	print(len(fingerings))
	print(fingerings[:3])

def test_c_maj_scale_down():
	c_maj_scale = converter.parse('./data/scales/cmaj.mxl')
	fingerings = finger_monotonic(c_maj_scale.parts[0].flat.notes[14:])
	print(len(fingerings))
	print(fingerings[:3])

def test_b_maj_scale_down():
	b_maj_scale = converter.parse('./data/scales/bmaj.mxl')
	fingerings = finger_monotonic(b_maj_scale.parts[0].flat.notes[14:])
	print(len(fingerings))
	print(fingerings[:3])

def test_f_maj_scale_down():
	f_maj_scale = converter.parse('./data/scales/fmaj.mxl')
	fingerings = finger_monotonic(f_maj_scale.parts[0].flat.notes[14:])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_sharp_maj_scale_down():
	c_sharp_maj_scale = converter.parse('./data/scales/csharpmaj.mxl')
	fingerings = finger_monotonic(c_sharp_maj_scale.parts[0].flat.notes[14:])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_maj_arpeggio_up():
	c_maj_arpeggio = converter.parse('./data/arpeggios/cmaj.mxl')
	fingerings = finger_monotonic(c_maj_arpeggio.parts[0].flat.notes[:7])
	print(len(fingerings))
	print(fingerings[:5])

def test_a_maj_arpeggio_up():
	a_maj_arpeggio = converter.parse('./data/arpeggios/amaj.mxl')
	fingerings = finger_monotonic(a_maj_arpeggio.parts[0].flat.notes[:7])
	print(len(fingerings))
	print(fingerings[:3])

def test_b_maj_arpeggio_up():
	b_maj_arpeggio = converter.parse('./data/arpeggios/bmaj.mxl')
	fingerings = finger_monotonic(b_maj_arpeggio.parts[0].flat.notes[:7])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_sharp_maj_arpeggio_up():
	c_sharp_maj_arpeggio = converter.parse('./data/arpeggios/csharpmaj.mxl')
	fingerings = finger_monotonic(c_sharp_maj_arpeggio.parts[0].flat.notes[:7])
	print(len(fingerings))
	print(fingerings[:5])

def test_b_flat_min_arpeggio_up():
	b_flat_min_arpeggio = converter.parse('./data/arpeggios/bflatmin.mxl')
	fingerings = finger_monotonic(b_flat_min_arpeggio.parts[0].flat.notes[:7])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_maj_arpeggio_down():
	c_maj_arpeggio = converter.parse('./data/arpeggios/cmaj.mxl')
	fingerings = finger_monotonic(c_maj_arpeggio.parts[0].flat.notes[6:])
	print(len(fingerings))
	print(fingerings[:5])

def test_a_maj_arpeggio_down():
	a_maj_arpeggio = converter.parse('./data/arpeggios/amaj.mxl')
	fingerings = finger_monotonic(a_maj_arpeggio.parts[0].flat.notes[6:])
	print(len(fingerings))
	print(fingerings[:3])

def test_b_maj_arpeggio_down():
	b_maj_arpeggio = converter.parse('./data/arpeggios/bmaj.mxl')
	fingerings = finger_monotonic(b_maj_arpeggio.parts[0].flat.notes[6:])
	print(len(fingerings))
	print(fingerings[:3])

def test_c_sharp_maj_arpeggio_down():
	c_sharp_maj_arpeggio = converter.parse('./data/arpeggios/csharpmaj.mxl')
	fingerings = finger_monotonic(c_sharp_maj_arpeggio.parts[0].flat.notes[6:])
	print(len(fingerings))
	print(fingerings[:5])

def test_b_flat_min_arpeggio_down():
	b_flat_min_arpeggio = converter.parse('./data/arpeggios/bflatmin.mxl')
	fingerings = finger_monotonic(b_flat_min_arpeggio.parts[0].flat.notes[6:])
	print(len(fingerings))
	print(fingerings[:3])

def test_get_color():
	assert(get_color(note.Note('C4')) == 'white')
	assert(get_color(note.Note('C#4')) == 'black')

def show_c_maj_scale_up():
	c_maj_scale = converter.parse('./data/scales/cmaj.mxl')
	fingerings = finger_monotonic(c_maj_scale.parts[0].flat.notes[:15])
	new_score = annotate_score(c_maj_scale.parts[0], fingerings[0][0])
	new_score.show()

def show_c_sharp_maj_scale_down():
	c_sharp_maj_scale = converter.parse('./data/scales/csharpmaj.mxl')
	fingerings = finger_monotonic(c_sharp_maj_scale.parts[0].flat.notes[14:])
	new_score = annotate_score(c_sharp_maj_scale.parts[0], fingerings[0][0], offset=14)
	new_score.show()

# test_get_color()

# SCALES

# test_c_maj_scale_up()
# test_b_maj_scale_up()
# test_c_sharp_maj_scale_up()
# test_f_maj_scale_up()

# test_c_maj_scale_up_lh()
# test_b_maj_scale_up_lh()

# test_c_maj_scale_down()
# test_b_maj_scale_down()
# test_c_sharp_maj_scale_down()
# test_f_maj_scale_down()

# ARPEGGIOS

# test_c_maj_arpeggio_up()
# test_a_maj_arpeggio_up()
# test_b_maj_arpeggio_up()
# test_c_sharp_maj_arpeggio_up()
# test_b_flat_min_arpeggio_up()

# test_c_maj_arpeggio_down()
# test_a_maj_arpeggio_down()
# test_b_maj_arpeggio_down()
# test_c_sharp_maj_arpeggio_down()
# test_b_flat_min_arpeggio_down()

# show_c_maj_scale_up()
# show_c_sharp_maj_scale_down()

