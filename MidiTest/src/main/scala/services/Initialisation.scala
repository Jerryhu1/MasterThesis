package services

import models.{Bar, Note}
import constants.Constants
import models.Matrix.Matrix

import scala.annotation.tailrec
import scala.collection.mutable.ArrayBuffer
import scala.util.Random

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
    val population = new ArrayBuffer[Bar]

    for(i <- 0 until populationSize){
      var i = randomWalk(0, new Bar(), keys, matrix, Rng.rng)
      i.fitness = Constants.fitnessFunction(i)
      population += i
    }

    return population
  }

  @tailrec
  def randomWalk(size: Int = 0, bar: Bar, keys: IndexedSeq[(Note, Note)], matrix: Matrix, rng: Random) : Bar = {

    (size : Int, bar: Bar) match {
      // If the duration is longer than 1.0, trim and return
      case (_,b) if b.getDuration() >= 1.0 =>
        trimBar(b)
      // Start case
      case (s, b) if s == 0 && b != null =>
        val randomKey = Rng.rng.nextInt(keys.size - 1)
        val notes = keys.apply(randomKey)

        // TODO: Sample duration randomly, now taken from transition matrix
        bar.notes += notes._1
        bar.notes += notes._2
        randomWalk(size + 2, bar, keys, matrix, rng)
      case _ =>
        val note = getRandomTransition(matrix, bar.notes.last)
        bar.notes += note
        randomWalk(size+1, bar, keys, matrix, rng)
    }
  }

  def getRandomTransition(matrix : Matrix, startNote: Note) : Note = {
    val transitions = matrix.filter(item => startNote.equals(item._1._1))
    if(transitions.isEmpty){
      System.err.println(s"No transitions found for note: ${startNote.name}")
    }
    val rng = Rng.rng.nextDouble()
    var pCounter = 0.0

    for ((k,v) <- transitions) {
      // If the random number is inside the cumulative probability, take this transition
      if(rng > pCounter && rng < pCounter + v){
        return k._2
      }
      pCounter += v
    }
    // Should not be possible unless there is a probability not adding up to 1
    System.err.println(s"Probabilities of transitions of ${startNote} do not add up to one")
    null
  }


  def trimBar(bar: Bar) : Bar = {
    var difference = bar.getDuration() - 1.0
    while(difference > 0.0){

      val lastNote = bar.notes.last

      if(lastNote.duration - difference <= 0.0){
        bar.notes.remove(bar.notes.size-1)
      }
      else{
        lastNote.duration = lastNote.duration - difference
      }

      difference = bar.getDuration() - 1.0

    }
    return bar
  }
}

