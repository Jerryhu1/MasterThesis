package services

import models.Matrix.Matrix
import models.{Bar, Note}

import scala.collection.mutable.ArrayBuffer

object Initialisation {
  def initializePopulationRandomly(populationSize: Int, measureLength: Int) : ArrayBuffer[Bar] ={
    var population = new ArrayBuffer[Bar]
    for(i <- 0 until populationSize){
      val bar = new Bar()

      for(j <- 0 until measureLength){
        // Generate notes between C4 and C6
        val note = new Note(60 + Rng.rng.nextInt(10), Duration.getDuration())
        bar.notes += note
      }
      val fitness = Fitness.getFitness(bar)
      bar.fitness = fitness
      population += bar
    }

    population
  }

  def initializePopulationByModel() : ArrayBuffer[Bar] = {
    throw new NotImplementedError()
  }

  def populateTransitionMatrix() : Matrix = {
    val matrix = Array(Array)

  }
}
