'''
Variables storing comfort scores for fingerings of two notes.

Should have a score for each combination:
	(finger 1, finger 2, distance, color 1, color 2) where distance is in half steps.

For example, (1, 2, 3, 'white', 'black') corresponds to the comfort score of playing
a thumb on a white key, say C4, and an index finger on a black key three half steps 
above, say E-4.

Note that distance is always positive, indicating an ascending interval. We assume that
comfort is unaffected by direction, that is, 1 on C followed by 2 on E is as comfortable
as 2 on E followed by 1 on C. Currently, distance ranges from 0 to 12 (an octave).

Also note that finger pairings such as (3, 1) are included. This represents the thumb
crossing under the middle finger.

The scores are organized as a two layer dictionary. The outer layer specifies the step size
and colors of keys, and the inner layer specifies the finger pairing. If the finger pair
is not included, it is assumed to have a comfort score of 0.

Comfort scores are subjective, based on our own experience playing piano. In general, the 
following principles are followed:

	- Thumbs on black keys have lower scores.
	- Crossing the thumb under the ring finger or pinky has a low score.
	- Crossing the thumb under is only permissible for small distances.
	- Using the same finger twice in a row has a low score, unless the distance is 0.
	- The more the distance between fingers aligns with distance, the higher the score.

Future work:

	- Because we assume that comfort is unaffected by direction, we disallow fingerings
	  take advantage of sliding ones finger from a black key to a white key, as such
	  maneuvers are only valid in one direction.
	- These comfort scores are for playing notes consecutively, and do not necessarily 
	  carry over to playing two notes simultaneously. As such, our algorithm ignores
	  chords and replaces them with their highest note. In the future, we could explore
	  how to finger isolated chords, and then chords in the context of a piece of music.
'''
COMFORT = {
	(0, 'white', 'white'): {
		(1, 1): 10,
		(1, 2): 5,
		(1, 3): 4,
		(1, 4): 3,
		(1, 5): 2,
		(2, 1): 5,
		(2, 2): 10,
		(2, 3): 6,
		(2, 4): 2,
		(2, 5): 1,
		(3, 1): 4,
		(3, 3): 10,
		(3, 4): 5,
		(3, 5): 2,
		(4, 1): 3,
		(4, 4): 10,
		(4, 5): 4,
		(5, 5): 10,
	},
	(0, 'black', 'black'): {
		(1, 1): 9,
		(1, 2): 4,
		(1, 3): 3,
		(1, 4): 2,
		(1, 5): 1,
		(2, 1): 4,
		(2, 2): 10,
		(2, 3): 6,
		(2, 4): 2,
		(2, 5): 1,
		(3, 1): 3,
		(3, 3): 10,
		(3, 4): 5,
		(3, 5): 2,
		(4, 1): 2,
		(4, 4): 10,
		(4, 5): 4,
		(5, 5): 10,
	},

	(1, 'white', 'white'): {
		(1, 2): 10,
		(1, 3): 5,
		(1, 4): 3,
		(1, 5): 1,
		(2, 1): 7,
		(2, 3): 10,
		(2, 4): 5,
		(2, 5): 3,
		(3, 1): 8,
		(3, 4): 10,
		(3, 5): 5,
		(4, 1): 7,
		(4, 5): 10,
	},
	(1, 'white', 'black'): {
		(1, 2): 10,
		(1, 3): 8,
		(1, 4): 4,
		(1, 5): 2,
		(2, 3): 10,
		(2, 4): 4,
		(3, 4): 10,
		(3, 5): 3,
		(4, 5): 10,
	},
	(1, 'black', 'white'): {
		(1, 2): 5,
		(1, 3): 3,
		(1, 4): 1,
		(2, 1): 9,
		(2, 3): 10,
		(2, 4): 6,
		(2, 5): 4,
		(3, 1): 10,
		(3, 4): 10,
		(3, 5): 6,
		(4, 1): 8,
		(4, 5): 10,
	},

	(2, 'white', 'white'): {
		(1, 2): 10,
		(1, 3): 5,
		(1, 4): 3,
		(1, 5): 1,
		(2, 1): 7,
		(2, 3): 10,
		(2, 4): 5,
		(2, 5): 3,
		(3, 1): 8,
		(3, 4): 10,
		(3, 5): 5,
		(4, 1): 7,
		(4, 5): 10,
	},
	(2, 'white', 'black'): {
		(1, 2): 10,
		(1, 3): 9,
		(1, 4): 5,
		(1, 5): 3,
		(2, 3): 10,
		(2, 4): 9,
		(2, 5): 2,
		(3, 4): 10,
		(3, 5): 8,
		(4, 5): 10,
	},
	(2, 'black', 'white'): {
		(1, 2): 5,
		(1, 3): 4,
		(1, 4): 3,
		(2, 1): 7,
		(2, 3): 10,
		(2, 4): 6,
		(2, 5): 4,
		(3, 1): 8,
		(3, 4): 10,
		(3, 5): 6,
		(4, 1): 7,
		(4, 5): 10,
	},
	(2, 'black', 'black'): {
		(1, 2): 9,
		(1, 3): 5,
		(1, 4): 3,
		(1, 5): 1,
		(2, 1): 6,
		(2, 3): 10,
		(2, 4): 5,
		(2, 5): 3,
		(3, 1): 7,
		(3, 4): 10,
		(3, 5): 5,
		(4, 1): 6,
		(4, 5): 10,
	},

	(3, 'white', 'white'): {
		(1, 2): 9,
		(1, 3): 10,
		(1, 4): 8,
		(1, 5): 7,
		(2, 1): 7,
		(2, 3): 8,
		(2, 4): 10,
		(2, 5): 8,
		(3, 1): 7,
		(3, 4): 6,
		(3, 5): 10,
		(4, 1): 5,
		(4, 5): 6,
	},
	(3, 'white', 'black'): {
		(1, 2): 9,
		(1, 3): 10,
		(1, 4): 7,
		(1, 5): 3,
		(2, 3): 9,
		(2, 4): 10,
		(2, 5): 3,
		(3, 4): 8,
		(3, 5): 9,
		(4, 5): 7,
	},
	(3, 'black', 'white'): {
		(1, 2): 5,
		(1, 3): 4,
		(1, 4): 3,
		(2, 1): 7,
		(2, 3): 10,
		(2, 4): 6,
		(2, 5): 4,
		(3, 1): 8,
		(3, 4): 10,
		(3, 5): 6,
		(4, 1): 7,
		(4, 5): 10,
	},
	(3, 'black', 'black'): {		
		(1, 2): 9,
		(1, 3): 9,
		(1, 4): 5,
		(1, 5): 3,
		(2, 1): 5,
		(2, 3): 10,
		(2, 4): 10,
		(2, 5): 7,
		(3, 1): 6,
		(3, 4): 9,
		(3, 5): 10,
		(4, 1): 5,
		(4, 5): 9,
	},

	(4, 'white', 'white'): {
		(1, 2): 10,
		(1, 3): 10,
		(1, 4): 8,
		(1, 5): 7,
		(2, 1): 7,
		(2, 3): 9,
		(2, 4): 10,
		(2, 5): 8,
		(3, 1): 7,
		(3, 4): 6,
		(3, 5): 10,
		(4, 1): 5,
		(4, 5): 6,
	},
	(4, 'white', 'black'): {
		(1, 2): 10,
		(1, 3): 10,
		(1, 4): 9,
		(1, 5): 8,
		(2, 3): 7,
		(2, 4): 10,
		(2, 5): 9,
		(3, 4): 5,
		(3, 5): 10,
		(4, 5): 5,
	},
	(4, 'black', 'white'): {
		(1, 2): 4,
		(1, 3): 5,
		(1, 4): 4,
		(1, 5): 3,
		(2, 1): 6,
		(2, 3): 8,
		(2, 4): 10,
		(2, 5): 9,
		(3, 1): 7,
		(3, 4): 6,
		(3, 5): 10,
		(4, 1): 6,
		(4, 5): 5,
	},
	(4, 'black', 'black'): {
		(1, 2): 8,
		(1, 3): 9,
		(1, 4): 7,
		(1, 5): 5,
		(2, 1): 5,
		(2, 3): 9,
		(2, 4): 10,
		(2, 5): 7,
		(3, 1): 6,
		(3, 4): 7,
		(3, 5): 10,
		(4, 1): 5,
		(4, 5): 9,
	},

	(5, 'white', 'white'): {
		(1, 2): 9,
		(1, 3): 10,
		(1, 4): 10,
		(1, 5): 8,
		(2, 1): 6,
		(2, 3): 7,
		(2, 4): 10,
		(2, 5): 10,
		(3, 1): 6,
		(3, 4): 5,
		(3, 5): 10,
		(4, 1): 4,
		(4, 5): 6,
	},
	(5, 'white', 'black'): {
		(1, 2): 9,
		(1, 3): 10,
		(1, 4): 10,
		(1, 5): 8,
		(2, 3): 7,
		(2, 4): 10,
		(2, 5): 10,
		(3, 4): 5,
		(3, 5): 10,
		(4, 5): 5,
	},
	(5, 'black', 'white'): {
		(1, 2): 4,
		(1, 3): 5,
		(1, 4): 4,
		(1, 5): 3,
		(2, 1): 6,
		(2, 3): 8,
		(2, 4): 10,
		(2, 5): 10,
		(3, 1): 7,
		(3, 4): 6,
		(3, 5): 10,
		(4, 1): 6,
		(4, 5): 5,
	},
	(5, 'black', 'black'): {
		(1, 2): 8,
		(1, 3): 9,
		(1, 4): 9,
		(1, 5): 7,
		(2, 1): 5,
		(2, 3): 7,
		(2, 4): 10,
		(2, 5): 10,
		(3, 1): 5,
		(3, 4): 6,
		(3, 5): 10,
		(4, 1): 4,
		(4, 5): 6,
	},

	(6, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(6, 'white', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(6, 'black', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(6, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},

	(7, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(7, 'white', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(7, 'black', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(7, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},

	(8, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(8, 'white', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(8, 'black', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(8, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},

	(9, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(9, 'white', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(9, 'black', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(9, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},

	(10, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(10, 'white', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(10, 'black', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(10, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},

	(11, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(11, 'white', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(11, 'black', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(11, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},

	(12, 'white', 'white'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
	(12, 'black', 'black'): {
		(1, 1): 0,
		(1, 2): 0,
		(1, 3): 0,
		(1, 4): 0,
		(1, 5): 0,
		(2, 1): 0,
		(2, 2): 0,
		(2, 3): 0,
		(2, 4): 0,
		(2, 5): 0,
		(3, 1): 0,
		(3, 3): 0,
		(3, 4): 0,
		(3, 5): 0,
		(4, 1): 0,
		(4, 4): 0,
		(4, 5): 0,
		(5, 5): 0,
	},
}