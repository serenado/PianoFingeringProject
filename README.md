# Piano Fingering

## Background

The number of potential fingerings of a piano piece is exponential. A one-handed, two-octave scale alone has over 186 quintillion possibilities. Yet, despite this astronomical solution space, practiced pianists are able to intuitively generate appropriate piano fingerings, even on the fly for a piece they have never seen or heard before. 

When it comes to piano fingering, there generally isn't a right answer. Fingering choices can vary per pianist based on what is most comfortable for their own hands. Our task in this project was to reduce the exponential number of possible fingerings to a single fingering that would be as reasonable as possible.

In piano finger notation, the convention is to number the fingers of each hand 1 to 5 from thumb to pinky, as shown in the diagram below.

<img src="img/hands.jpg" height="200" align="center"/>

## Our Approach

The algorithm overview:
1. Create table of comfort scores for a pair of notes
2. Split each part into smaller chunks
3. Generate potential fingerings for each chunk
4. Stitch chunks together and find the most comfortable fingering

### Comfort score table

In order to judge whether a fingering is reasonable, our algorithm relies on a table of comfort scores. Given a pair of notes and fingers, the algorithm can lookup how comfortable on a scale from 1 to 10 that transition is. 

When deciding fingering, pianists take into account many factors, but the two most important are distance between notes, and the color of the piano keys. Thus, our comfort score table has an entry for every combination of `(distance, color 1, color 2, finger 1, finger 2)`, where distance is measured in half steps and fingers are for the right hand.

For example, `(3, 'white', 'black', 1, 2)` corresponds to the comfort score of playing a thumb on a white key, say C4, and an index finger on a black key three half steps above, say E-4.

Note that distance is always positive, indicating an ascending interval. We assume that comfort is unaffected by direction, that is, 1 on C followed by 2 on E is as comfortable as 2 on E followed by 1 on C. We also assume symmetry between hands.

Also note that finger pairings such as `(3, 1)` are included. This represents the thumb crossing under the middle finger.

The scores are organized as a two layer dictionary. The outer layer specifies the step size and colors of keys, and the inner layer specifies the finger pairing. If the finger pair is not included, it is deemed an unacceptable fingering and will never appear in a fingering
produced by our algorithm. Note that this means it is possible to construct songs with no valid fingerings, if they require movements that we have deemed unacceptable.

Comfort scores are subjective, based on our own experience playing piano. In general, we adhered to the following principles:
- Thumbs on black keys have lower scores.
- Crossing the thumb under the pinky is unacceptable.
- Crossing the thumb under is only permissible for small distances.
- Using the same finger twice in a row is unacceptable, unless the distance is 0.
- The more the distance between fingers aligns with distance between piano keys, the higher the score.
- For intervals with the same physical distance but different half-step distances, comfort scores should be the same. For example, C4 and E4 have the same physical distance as D4 and F4, but more half steps between them.

### Splitting into chunks

Scores were first pre-processed in order to remove chord tones because the algorithm currently cannot handle chords. For the left hand, we removed all tones except for the lowest note. For the right hand, we kept the highest note. These parts were then split into ascending and descending chunks. Adjacent chunks share a transition note which is the local maxima or minima in pitch space. 

To give more fingering options when rests are present in the score, users have the option of specifying if rests should be used as chunk splits. There is a flag that determines if rests should be ignored or specifies the minimum length rest (in quarter beats) for a rest to be used as a chunk split. The ability to specify a minimum rest length accounts for the fact that tempo affects how easily a pianist can reset during rests. 

[k545_chunks]: img/k545_chunks.png
In the following excerpt from Piano Sonata No. 16 in C major, K. 545, by Mozart, ascending chunks are blue and descending chunks are orange. Rests with duration greater than 1 quarter beat were used as resets.
![Mozart, K.545 Excerpt][k545_chunks]

### Fingering a single chunk

Once we have split a score into ascending and descending chunks, we need a way to find potential fingerings for each chunk, as well as how comfortable each one is. Our algorithm for doing so is quite simple. We simply use the comfort score table along with a BFS approach to generate all potential fingerings. 

That is, for each partial fingering we have so far, consider playing the next note with every finger. Then, we refer to our comfort score table. If that note transition is acceptable, we update our list of partial fingerings as well as the total comfort score for that fingering. Once we are finished, we divide each total score by the number of note transitions to obtain an average comfort score.

In order to use the comfort table correctly, we also make sure to check whether the chunk is ascending or descending, and which hand we are working with. Because the comfort table is for ascending pairs of notes, we merely reverse the order of the notes and fingers to turn a descending pair into an ascending one. For the left hand, we reverse the order of fingers as well as the colors of keys to match the reflective symmetry of hands.

Because the comfort score table only contains entries for acceptable finger transitions, the fingerings generated by this algorithm will all be acceptable, although some may be more comfortable than others.

### Stitching together chunks

As described in the previous section, each chunk has a list of fingering options with associated scores. To stitch these chunks together, a dynamic programming algorithm was used which optimizes over the total comfort score under the constraint that the last note of each chunk is assigned the same finger as the first note of the following chunk (i.e. the transition note is assigned to the same finger). With this constraint, we ensure that we are only combining compatible fingerings.   

The dynamic programming problem is structured as: 
`d[i][j] = best score after i chunks where chunk i ends on finger j`

Subproblems are related as `d[i+1][j] = max over e in [1...5] (d[i][e] + s[i+1])` where s[i+1] is the comfort score of a fingering option for chunk i+1 that starts on finger e and ends on finger j. For the base case, d[0][j] is the score of a fingering option that ends on finger j for the first chunk.

The solution for an entire score would be the best solution to `d[len(chunks)][j]` where j can be any finger since we have no constraint over the last finger used in a piece. The final solution returns a fingering and a total comfort score. This total comfort score can be scaled by dividing by 10 * len(chunks) which gives a rating from 0 to 1 for result of the algorithm. 


## Results

Results of our algorithm are in the /results directory. Some examples of output with the corresponding normalized score are:

[k545_result]: img/k545.png
[b_maj_result]: img/bmaj.png
[c_maj_result]: img/cmaj.png

![B Major results][b_maj_result]
![Mozart, K.545 Results][k545_result]
RH: 0.976
LH: 0.984

The algorithm will sometimes return a functional fingering but one that most piano players would not prefer to play. For example, in the C major chord shown below, the descending chunk ends in 3214321 while most piano players would mostly likely finger it as 4321321. 
![C Major results][c_maj_result]
The score for the C major scale is only 0.95 while the B major scale was 0.976 for the right hand.

## Future Work

There are a lot of aspects and nuances of piano music that our algorithm does not yet capture. Some of those include:
- Chords
- Ornaments (trills, turns, grace notes, etc.)
- Rests
	- Long enough rests serve as an opportunity for the pianist to pick up their hand and move to another area of the keyboard. There is some nuance to this as it is often more convenient to leave the hand in place. In addition, the length of the rest may correspond with how far the pianist is able to move in that time.
- Fancy maneuvers
	- Ornaments like trills, turns, grace notes, etc.
	- Crossing hands over each other
	- Playing two notes with one thumb simultaneously
	- Holding a note while playing other notes in the same hand
	- Switching fingers while holding a long note
	- Switch fingers while repeatedly playing a note

<div align="center">
<img src="img/trill.jpg" height="250"/>
<br/>
<i>An interesting cascading trill (Chopin's Polonaise Op. 40, No. 1)</i>
</div>

<div align="center">
<img src="img/double_thumb.jpg" height="250"/>
<br/>
<i>A chord where the thumb bridges across two notes (Chopin's Prelude Op. 28, No. 20)</i>
</div>

<div align="center">
<img src="img/finger_swap.jpg" height="200"/>
<br/>
<i>Starting a note on one finger and switching to another while holding it down (Chopin's Prelude Op. 28, No. 6)</i>
</div>

<div align="center">
<img src="img/repeated.jpg" height="220"/>
<br/>
<i>Repeated notes benefit from switching fingers to maintain an even beat (Chopin's Prelude Op. 28, No. 15)</i>
</div>
