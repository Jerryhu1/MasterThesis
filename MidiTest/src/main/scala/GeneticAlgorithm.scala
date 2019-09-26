import constants.Constants
import csv.MatrixReader
import models.Matrix.Matrix
import models.{Bar, Note}
import org.jfugue.pattern.Pattern
import org.jfugue.player.Player
import services._

import scala.collection.mutable.ArrayBuffer
import scala.language.postfixOps
import services.Rng.rng

import scala.collection.mutable

class GeneticAlgorithm {


  var population = new ArrayBuffer[Bar]

  def run() : Unit = {

    System.out.println("Initialising population...")

    var matrix = MatrixReader.getTransitionMatrixFromFile
    population = Initialisation.initializePopulationByModel(matrix, Constants.populationSize)

    System.out.println(s"Done initialising, Starting evolution, doing ${Constants.iterations} iterations")

    for(i <- 0 until Constants.iterations){
      // Selection
      //val selectedPopulation = Constants.selection(population)
      //population = new ArrayBuffer[Bar]

      // Repopulation
      // Update matrix with selection
      //matrix = MatrixUpdater.updateMatrix(selectedPopulation, matrix)

      // Sample new population from updated matrix
      //val samplePopulation = Initialisation.initializePopulationByModel(matrix, Constants.samplePopulationSize)

      // Get new population from crossover and mutation
     // population = selectionCrossoverMutation

//      for(i <- selectedPopulation.indices by 2) {
//        val (c1,c2) = Constants.crossover(selectedPopulation(i), selectedPopulation(i+1))
//        Constants.mutation(c1)
//        Constants.mutation(c2)
//        c1.fitness = Constants.fitnessFunction(c1)
//        c2.fitness = Constants.fitnessFunction(c2)
//        population += c1
//        population += c2
//      }

      //population ++= samplePopulation

      System.out.println(s"Iteration $i done: " +
        s"\n Average fitness: ${population.foldLeft(0){ (acc, i) => acc + i.fitness} / Constants.populationSize}" +
        s"\n Max fitness: ${population.map(_.fitness).max}")
    }

    // Play music
    play()

  }

  def jfugueTest(): Unit ={
    val pattern = new Pattern()
    val rest = new org.jfugue.theory.Note("R")
    rest.setDuration(0.125)
    pattern.add("V2 I[Piano] C5q Rq D5q F5q")
    pattern.add(rest)
    System.out.println(pattern.toString)
    val player = new Player()

    player.play(pattern)
  }

  private def play() = {
    System.out.println("Done with evolving, playing....")

    val bars = population.sortBy(x => x.fitness).reverse
    for (bar: Bar <- bars.take(5)) {
     // val pattern = bar.convertToPattern(1, "Piano", Constants.tempo)
      //System.out.println(s"Playing pattern ${pattern.toString} with fitness: ${bar.fitness}")
      var pattern = new Pattern()
      pattern.add("V2 I[Piano] C4majw C4majw C4majw C4majw Cmajw C4maj4w Cmajw")
      val player = new Player()

      player.play(pattern)
    }
  }

  private def selectionCrossoverMutation() : ArrayBuffer[Bar] = {
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

}
