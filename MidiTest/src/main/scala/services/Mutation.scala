package services

import models.Bar

import scala.util.Random

object Mutation {
  val rng = new Random()

  def applyMutation(individual: Bar) : Unit = {
    val operatorIdx = rng.nextInt(1)

    operatorIdx match {
      case 0 => swapNotes(individual)
      case 1 => changePitch(individual)
    }
  }

  def swapNotes(individual: Bar): Unit ={
    var firstIdx = rng.nextInt(individual.notes.length-1)
    val secondIdx = rng.nextInt(individual.notes.length-1)
    while(firstIdx == secondIdx){
      firstIdx = rng.nextInt(individual.notes.length-1)
    }
    val firstNote = individual.notes(firstIdx)
    val secondNote = individual.notes(secondIdx)

    individual.notes(firstIdx) = secondNote
    individual.notes(secondIdx) = firstNote
  }

  def changePitch(individual: Bar) : Unit = {
    var index = rng.nextInt(individual.notes.length-1)
    var tone = rng.nextInt(7)
    individual.notes(index) = Fitness.CMajorScale(tone)
  }
}
