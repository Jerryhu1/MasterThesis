package services

import models.{Bar, Note}

class Fitness
object Fitness {
  val CMajorScale = List(
    Note.fromNoteString("C6", 0.125),
    Note.fromNoteString("D6", 0.125),
    Note.fromNoteString("E6", 0.125),
  )
  def getFitness(bar: Bar): Double ={
    //Switch case for fitness method
    var fitness = 0.0

    for(note <- bar.notes){
      if(CMajorScale.map(x => x.note).contains(note.note) || note.name == "R" ){
        fitness += 1.0
      }
    }

    fitness / bar.notes.length
  }
}
