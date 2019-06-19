package services

import models.{Bar, Note}

class FitnessService
object FitnessService {
  val CMajorScale = List(
    Note.fromNoteString("C5", 0.125),
    Note.fromNoteString("D5", 0.125),
    Note.fromNoteString("E5", 0.125),
    Note.fromNoteString("F5", 0.125),
    Note.fromNoteString("G5", 0.125),
    Note.fromNoteString("A5", 0.125),
    Note.fromNoteString("B5", 0.125),

  )
  def getFitness(bar: Bar): Int ={
    //Switch case for fitness method

    var fitness = 0

    for(note <- bar.notes){
      if(CMajorScale.map(x => x.note).contains(note.note)){
        fitness += 1
      }
    }

    fitness
  }
}
