'''
Variable storing comfort scores for fingerings of two notes.

Should have a score for each combination:
	(finger 1, finger 2, distance, color 1, color 2) where distance is in half steps

For example, (1, 2, 3, 'white', 'black') corresponds to the comfort score of playing
a thumb on a white key, say C4, and an index finger on a black key three half steps 
above, say E-4.
'''
COMFORT = {}