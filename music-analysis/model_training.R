install.packages("tuneR")
library(tuneR)

#setwd("B://Projects//MasterThesis//music-analysis")
setwd("C://School//Master//Thesis//Programming//MasterThesis//music-analysis")
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
notes_track2 <- midi_notes[match(data$events_track2.parameter1, key),]$notes


#Initialize frequency vector
track1_note_frequency <- matrix(rep(0, length(midi_notes)), nrow=1, ncol=length(midi_notes$notes))
colnames(track1_note_frequency) <- midi_notes$notes
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
transition_matrix <- t(t(transition_matrix) / track1_note_frequency[1,])



#Trains a transition matrix given a corpus and all possible notes. 
train.transitionMatrix <- function(corpus, possibleNotes){
  
  transition_matrix <- matrix(rep(0,length(possibleNotes)*length(possibleNotes)), nrow=length(possibleNotes), ncol=length(possibleNotes))
  dimnames(transition_matrix) <- list(possibleNotes, possibleNotes)
  frequency_vector <- matrix(rep(0, length(possibleNotes)), nrow=1, ncol=length(possibleNotes))
  for(i in 1:length(corpus)){
    curr <- corpus[[i]]
    #Take the notes of current song and get frequency vector
    frequency_vector <- frequencyVector(frequency_vector, possibleNotes, notes = curr)
    #Update the transition matrix by this current song
    transition_matrix <- transitionMatrix(transition_matrix, possibleNotes, curr)
  }
  # Divide by frequency vector
  transition_matrix <- t(t(transition_matrix) / frequency_vector[1,])
  transition_matrix[is.nan(transition_matrix)] <- 0
  return(transition_matrix)
}

#Creates or updates the transition matrix given its 1-gram frequency matrix, all possible notes vector and the given notes vector
transitionMatrix <- function(transition_matrix, possibleNotes, notes){
  #Initialize transition matrix
  #TODO: Add initial note, so start note without any posterior
  if(is.null(transition_matrix)){
    transition_matrix <- matrix(rep(0,length(possibleNotes)*length(possibleNotes)), nrow=length(possibleNotes), ncol=length(possibleNotes))
    #Add dimension names
    dimnames(transition_matrix) <- list(possibleNotes, possibleNotes)
  }
  
  for(i in 1:length(notes)){
    if(i == 1){next;}
    
    prev <- notes[i-1]
    curr <- notes[i]
    
    transition_matrix[curr,prev] <- transition_matrix[curr,prev] + 1
  }
  
  #Divide by univariate frequency to get probabilities
  #transition_matrix <- t(t(transition_matrix) / frequencyVector[1,])
  return(transition_matrix)
}

#Creates or updates a frequency vector given the possible notes and sequence of notes
frequencyVector<- function(note_frequency, possibleNotes, notes){
  if(is.null(note_frequency)){
    #Initialize frequency vector
    note_frequency <- matrix(rep(0, length(possibleNotes)), nrow=1, ncol=length(possibleNotes))
    #Set dimension names by the possible notes vector
    colnames(note_frequency) <- possibleNotes
    #Fill up frequency vector
    for(i in 1:length(notes)){
      curr <- notes[i]
      note_frequency[curr] <- note_frequency[curr] + 1
    }
    return(note_frequency)
  }

  #Fill up frequency vector
  for(i in 1:length(notes)){
    curr <- notes[i]
    note_frequency[curr] <- note_frequency[curr] + 1
  }
  return(note_frequency)
}

# Read all files in given folder relative to the workspace
getCorpus <- function(folderName){
  files <- list.files(folderName, pattern="*.mid", full.names=TRUE)
  return(lapply(files, readMidi))
}

#Gets the notes for a specific item
getNotesForItem <- function(item, midi_notes){
      # Get all note on events
    note_on <- item[which(item$event=="Note On"),]
    # Get notes from the events as a sequence
    notes <- midi_notes[match(note_on$parameter1, key),]$notes
    return(notes)
}
