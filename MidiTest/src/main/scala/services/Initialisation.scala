package services

import models.{Bar, Note}
import constants.Constants
import models.Matrix.Matrix

import scala.annotation.tailrec
import scala.collection.mutable.ArrayBuffer

object Initialisation {

  def initializePopulationRandomly() : ArrayBuffer[Bar] ={
    var population = new ArrayBuffer[Bar]
    for(i <- 0 until Constants.populationSize){
      val bar = new Bar()

      for(j <- 0 until Constants.measureLength){
        // Generate notes between C4 and C6
        val note = new Note(60 + Rng.rng.nextInt(10), Duration.getDuration(), "")
        bar.notes += note
      }

      val fitness = Fitness.getFitness(bar)
      bar.fitness = fitness
      population += bar
    }
    return population
  }

  def initializePopulationByModel(matrix: Matrix, populationSize: Int) : ArrayBuffer[Bar] = {
    val keys = matrix.keys.toIndexedSeq
    val random = Rng.rng.nextInt(keys.size-1)
    val population = new ArrayBuffer[Bar]

    for(i <- 0 until Constants.populationSize){
      population += randomWalk(0, new Bar(), keys, matrix)
    }

    return population
  }

  @tailrec
  def randomWalk(size: Int = 0, bar: Bar, keys: IndexedSeq[(Note, Note)], matrix: Matrix) : Bar = {
    (size : Int, bar: Bar) match {
      //TODO: Replace hardcoded 32 with measure length
      // End case
      case (s, b) if s >= 32 && b != null => b
      // Start case
      case (s, b) if s == 0 && b != null =>
        val randomKey = Rng.rng.nextInt(keys.size - 1)
        val notes = keys.apply(randomKey)

        // TODO: Sample duration randomly, now taken from transition matrix
        bar.notes += notes._1
        bar.notes += notes._2
        randomWalk(size + 2, bar, keys, matrix)
      case _ =>
        val (t1,t2) = getRandomTransition(matrix, bar.notes.last)
        if(t2 == null){
          val x = 2
        }
        bar.notes += t2
        randomWalk(size+1, bar, keys, matrix)
    }
  }

  def getRandomTransition(matrix : Matrix, startNote: Note) : (Note, Note) = {
    val transitions = matrix.filter(item => startNote.equals(item._1._1))
    val rng = Rng.rng.nextDouble()
    var pCounter = 0.0

    for ((k,v) <- transitions) {
      // If the random number is inside the cumulative probability, take this transition
      if(rng > pCounter && rng < pCounter + v){
        if(k._2 == null){
          val x = 2
        }
        return (k._1, k._2)
      }
      pCounter += v
    }
    // Should not be possible
    null
  }

}

