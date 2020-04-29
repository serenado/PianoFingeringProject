from music21 import *
import constants

'''
TODO: introduce pruning to only keep best fingerings?
TODO: favor fingerings that start on 1, end on 5 for ascending, start on 5, end on 1 for descending?
TODO: may need a better way of associating fingers to notes
TODO: average scores over notes?
'''
def finger_monotonic(notes):
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

		distance = note.pitch.ps - prev_note.pitch.ps
		color = get_color(note)
		if distance >= 0:
			finger_pairs = constants.COMFORT[(abs(distance), prev_color, color)]
		else:
			finger_pairs = constants.COMFORT[(abs(distance), color, prev_color)]


		# for each partial fingering, try possible next fingers
		for fingering, score in fingerings:
			prev_finger = fingering[-1]
			for finger in [1, 2, 3, 4, 5]:
				if distance >= 0:
					finger_pair = (prev_finger, finger)
				else:
					finger_pair = (finger, prev_finger)
				if finger_pair in finger_pairs:
					comfort_score = finger_pairs[finger_pair]
					new_fingerings.append((fingering + [finger], score + comfort_score))

		fingerings = new_fingerings
		prev_note = note
		prev_color = color
	
	return sorted(fingerings, key=lambda x: x[1], reverse=True)

def get_color(note):
	if note.pitch.pitchClass in [0, 2, 4, 5, 7, 9, 11]:
		return 'white'
	return 'black'

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

def test_get_color():
	assert(get_color(note.Note('C4')) == 'white')
	assert(get_color(note.Note('C#4')) == 'black')

# test_get_color()

# test_c_maj_scale_up()
# test_b_maj_scale_up()
# test_c_sharp_maj_scale_up()
# test_f_maj_scale_up()

# test_c_maj_scale_down()
# test_b_maj_scale_down()
# test_c_sharp_maj_scale_down()
# test_f_maj_scale_down()
