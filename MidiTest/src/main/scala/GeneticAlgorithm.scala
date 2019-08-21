import models.Matrix.Matrix
import models.{Bar, Note}
import org.jfugue.player.Player
import services.{Crossover, Duration, Fitness, Mutation}

import scala.collection.mutable.ArrayBuffer
import scala.language.postfixOps
import services.Rng.rng

class GeneticAlgorithm(val populationSize: Int, val iterations: Int) {

  val measureLength = 32
  val tempo = 120

  var population = new ArrayBuffer[Bar]
  var transitionMatrix = new Matrix

  def run() : Unit = {

    System.out.println("Initialising population...")
    initializePopulation(populationSize)

    System.out.println(s"Done initialising, Starting evolution, doing $iterations iterations")
    for(i <- 0 until iterations){
      selectionCrossoverMutation()
    }

    System.out.println("Done with evolving, playing....")

    for(bar : Bar <- population.sortBy(x => x.fitness).reverse.take(5)){
      val pattern = bar.convertToPattern(1, "Piano", tempo)
      System.out.println(s"Playing pattern ${pattern.toString} with fitness: ${bar.fitness}")
      pattern.add("V2 I[Piano] C4majw D4majw E4minw C4majw Gmajw D4maj4w Cmajw")
      val player = new Player()

      player.play(pattern)
    }
  }

  def initializePopulation(populationSize: Int) : Unit ={
    population = new ArrayBuffer[Bar]
    for(i <- 0 until populationSize){
      val bar = new Bar()

      for(j <- 0 until measureLength){
        // Generate notes between C4 and C6
        val note = new Note(60 + rng.nextInt(10), Duration.getDuration())
        bar.notes += note
      }
      val fitness = Fitness.getFitness(bar)
      bar.fitness = fitness
      population += bar
    }
  }

  def selectionCrossoverMutation() : ArrayBuffer[Bar] = {
    var nextGeneration = new ArrayBuffer[Bar]
    for(i <- 0 until populationSize by 4){
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

    nextGeneration

  }


}
