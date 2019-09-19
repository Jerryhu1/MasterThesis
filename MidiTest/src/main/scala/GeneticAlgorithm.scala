import constants.Constants
import csv.MatrixReader
import models.Matrix.Matrix
import models.{Bar, Note}
import org.jfugue.player.Player
import services._

import scala.collection.mutable.ArrayBuffer
import scala.language.postfixOps
import services.Rng.rng

import scala.collection.mutable

class GeneticAlgorithm() {


  var population = new ArrayBuffer[Bar]

  def run() : Unit = {

    System.out.println("Initialising population...")

    val matrix = MatrixReader.getTransitionMatrixFromFile
    population = Initialisation.initializePopulationByModel(matrix, 10)

    System.out.println(s"Done initialising, Starting evolution, doing ${Constants.iterations} iterations")

    for(_ <- 0 until Constants.iterations){
      selectionCrossoverMutation()
    }

    System.out.println("Done with evolving, playing....")

    for(bar : Bar <- population.sortBy(x => x.fitness).reverse.take(5)){
      val pattern = bar.convertToPattern(1, "Piano", Constants.tempo)
      System.out.println(s"Playing pattern ${pattern.toString} with fitness: ${bar.fitness}")
      pattern.add("V2 I[Piano] C4majw D4majw E4minw C4majw Gmajw D4maj4w Cmajw")
      val player = new Player()

      player.play(pattern)
    }
  }

  def selectionCrossoverMutation() : ArrayBuffer[Bar] = {
    var nextGeneration = new ArrayBuffer[Bar]
    for(i <- 0 until Constants.populationSize by 4){
      // Selection
      val parents = population.slice(i, i + 4).sortBy(x => x.fitness)
      val children = new ArrayBuffer[Bar]
      // Crossover
      for(j <- parents.indices by 2){
        val newChildren = Crossover.onePoint(parents(j), parents(j+1))
        //Mutation
        Mutation.applyMutation(newChildren._1)
        newChildren._1.fitness = Fitness.getFitness(newChildren._1)
        Mutation.applyMutation(newChildren._2)
        newChildren._2.fitness = Fitness.getFitness(newChildren._2)
        children += newChildren._1
        children += newChildren._2
      }

      // Add to next generation
      val family = new ArrayBuffer[Bar]
      for(i <- 0 until 4){
        family += parents(i)
        family += children(i)
      }
      for(ind <- family.sortBy(x => x.fitness).reverse.take(4)){
        nextGeneration += ind
      }
    }
    return nextGeneration
  }

  def updateModel(matrix: Matrix) : Matrix = {
    for(i <- population){

    }
  }


}
