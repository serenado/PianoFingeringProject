# Piano Fingering

Given a piano score, our goal for this project was to produce a reasonable fingering.

## Background

put stuff about piano fingering for those who don't play piano

discuss past work maybe?

## Our Approach

The algorithm overview:
1. Create table of comfort scores for a pair of notes
2. Split each part into smaller chunks
3. Generate potential fingerings for each chunk
4. Stitch chunks together and find the most comfortable fingering

### Comfort scores and monotonic fingering

### Splitting and dynamic programming

## Results

maybe highlight where our fingerings differ from actual

## Future Work

There are a lot of aspects and nuances of piano music that our algorithm does not yet capture. Some of those include:
- Chords
- Ornaments (trills, turns, grace notes, etc.)
- Rests
	- Long enough rests serve as an opportunity for the pianist to pick up their hand and move to another area of the keyboard. There is some nuance to this as it is often more convenient to leave the hand in place. In addition, the length of the rest may correspond with how far the pianist is able to move in that time.
- Fancy maneuvers
	- Glissandos
	- Crossing hands over each other
	- Playing two notes with one thumb simultaneously
	- Holding a long note while playing other notes in the same hand
	- Switching fingers while holding a long note
