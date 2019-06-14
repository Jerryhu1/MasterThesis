package services

import models.Bar
import org.jfugue.theory._

class FitnessService
object FitnessService {
  val CMajorScale = List(
    new Note("C5"),
    new Note("D5"),
    new Note("E5"),
    new Note("F5"),
    new Note("G5"),
    new Note("A6"),
    new Note("B7")
  )
  def getFitness(bar: Bar): Int ={
    //Switch case for fitness method

    var fitness = 0

    for(note <- bar.pattern.get){

    }
  }
}
