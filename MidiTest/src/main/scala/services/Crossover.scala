package services

import models.Bar

import scala.util.Random

object Crossover {

  val rng = new Random()

  def onePoint(p1: Bar, p2: Bar) : (Bar,Bar) = {
    var point = rng.nextInt(p1.notes.length)
    var c1 = new Bar()
    var c2 = new Bar()

    for(i <- 0 until point){
      c1.notes += p2.notes(i)
      c2.notes += p1.notes(i)
    }
    for(i <- point until p1.notes.length){
      c1.notes += p1.notes(i)
      c2.notes += p2.notes(i)
    }
    Fitness.getFitness(c1)
    Fitness.getFitness(c2)

    (c1,c2)
  }
}
