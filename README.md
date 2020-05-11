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
(maybe move monotonic fingering to aftr splitting?)

### Splitting into chunks
Scores were first pre-processed in order to remove chord tones because the algorithm currently cannot handle chords. For the left hand, we removed all tones except for the lowest note. For the right hand, we kept the highest note. These parts were then split into ascending and descending chunks. Adjacent chunks share a transition note which is the local maxima or minima in pitch space. 

To give more fingering options when rests are present in the score, users have the option of specifying if rests should be used as chunk splits. There is a flag that determines if rests should be ignored or specifies the minimum length rest (in quarter beats) for a rest to be used as a chunk split. The ability to specify a minimum rest length accounts for the fact that tempo affects how easily a pianist can reset during rests. 

[k545_chunks]: img/k545_chunks.png
In the following excerpt from Piano Sonata No. 16 in C major, K. 545, by Mozart, ascending chunks are blue and descending chunks are orange. Rests with duration greater than 1 quarter beat were used as resets.
![Mozart, K.545 Excerpt][k545_chunks]

### Stitching together chunks
Each chunk has a list of fingering options with associated scores. To stich these chunks together, a dynamic programming algorithm was used which optimizes over the total comfort score under the constrant that the last note of each chunk is assigned the same finger as the first note of the following chunk (i.e. the transition note is assigned to the same finger). With this constraint, we ensure that we are only putting combining compatible fingerings.   

The dynamic programming problem is structured as: 
`d[i][j] = best score after i chunks where chunk i ends on finger j`

Subproblems are related as `d[i+1][j] = max over e in [1...5] (d[i][e] + s[i+1])` where s[i+1] is the comfort score of a fingering option for chunk i+1 that starts on finger e and ends on finger j. For the base case, d[0][j] is the score of a fingering option that ends on finger j for the first chunk.

The solution for an entire score would be the best solution to `d[len(chunks)][j]` where j can be any finger since we have no constraint over the last finger used in a piece. The final solution returns a fingering and a total comfort score. This total comfort score can be scaled by dividing by 10 * len(chunks) which gives a rating from 0 to 1 for result of the algorithm. 


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
