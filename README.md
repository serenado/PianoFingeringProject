# Piano Fingering






Future work:

- Because we assume that comfort is unaffected by direction, we disallow fingerings
  take advantage of sliding ones finger from a black key to a white key, as such
  maneuvers are only valid in one direction.
- These comfort scores are for playing notes consecutively, and do not necessarily 
  carry over to playing two notes simultaneously. As such, our algorithm ignores
  chords and replaces them with their highest note. In the future, we could explore
  how to finger isolated chords, and then chords in the context of a piece of music.