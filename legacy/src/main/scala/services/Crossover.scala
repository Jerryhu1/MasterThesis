package services

import models.Bar

import scala.util.Random

object Crossover {

  val rng = new Random()

  def onePoint(p1: Bar, p2: Bar) : (Bar,Bar) = {
    val point1 = rng.nextInt(p1.notes.length-1)
    val point2 = rng.nextInt(p2.notes.length-1)
    val c1 = new Bar()
    val c2 = new Bar()

    for(i <- 0 until point1){
      c1.notes += p1.notes(i)
    }
    for(i <- point2 until p2.notes.length){
      c1.notes += p2.notes(i)
    }

    for(i <- 0 until point2){
      c2.notes += p2.notes(i)
    }
    for(i <- point1 until p1.notes.length){
      c2.notes += p1.notes(i)
    }


    Fitness.getFitness(c1)
    Fitness.getFitness(c2)

    (c1,c2)
  }
}
