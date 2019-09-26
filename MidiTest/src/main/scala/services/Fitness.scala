package services

import models.{Bar, Note}

class Fitness
object Fitness {
  val CMajorScale = List(
    Note.fromNoteString("C6", 0.125),
    Note.fromNoteString("D6", 0.125),
    Note.fromNoteString("E6", 0.125),
    Note.fromNoteString("F6", 0.125),
    Note.fromNoteString("G6", 0.125),
    Note.fromNoteString("A6", 0.125),
    Note.fromNoteString("B6", 0.125),

  )
  def getFitness(bar: Bar): Int ={
    //Switch case for fitness method
    var fitness = 0

    for(note <- bar.notes){
      if(CMajorScale.map(x => x.note).contains(note.note) || note.name == "R" ){
        fitness += 1
      }
    }

    fitness
  }
}
