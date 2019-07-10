install.packages("tuneR")
library(tuneR)

setwd("B://Projects//MasterThesis//music-analysis")
song <- readMidi("chopin-no2.mid")
midi_notes <- read.csv("midi-notes.csv")

# Get all note on events
note_on <- song[which(song$event=="Note On"),]
#Get events from tracks 
events_track1 <- note_on[which(note_on$track == 1),]
events_track2 <- note_on[which(note_on$track == 2),]
# Map events to midi notes
key <- midi_notes$number
data <- data.frame(events_track1$parameter1)

# Get notes from the events as a sequence
notes_track1 <- midi_notes[match(data$events_track1.parameter1, key),]$notes
notes_track2 <- midi_notes[match(data$events_track2.parameter1, key),]$notes.

#Initialize frequency vector
track1_note_frequency <- matrix(rep(0, length(midi_notes)), nrow=1, ncol=length(midi_notes))

#Fill up frequency vector
for(i in 1:length(notes_track1)){
  
  curr <- notes_track1[i]
  track1_note_frequency[curr] <- track1_note_frequency[curr] + 1
}

#Initialize transition matrix
#TODO: Add initial note, so start note without any posterior
transition_matrix <- matrix(rep(0,length(midi_notes)*length(midi_notes)), nrow=length(midi_notes$notes), ncol =length(midi_notes$notes))
#Add dimension names
dimnames(transition_matrix) <- list(midi_notes$notes, midi_notes$notes)



for(i in 1:length(notes_track1)){
  if(i == 1){next;}
  
  prev <- notes_track1[i-1]
  curr <- notes_track1[i]
  
  transition_matrix[curr,prev] <- transition_matrix[curr,prev] + 1
}

#Divide by univariate frequency to get probabilities