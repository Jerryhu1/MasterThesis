import models.Bar
import org.jfugue.pattern.Pattern
import org.jfugue.player.Player
import org.jfugue.theory._

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer
import scala.util.Random

class GeneticAlgorithm {

  val rng = new Random()
  val measureLength = 8
  val tempo = 120

  var population = new ArrayBuffer[Bar]

  def run(populationSize: Int, iterations: Int) : Unit = {
      for(i <- 0 until iterations){
        initializePopulation(populationSize)
        for(bar : Bar <- population){
          System.out.println(s"Playing pattern: $i")
          val player = new Player()
          player.play(bar.pattern)
        }
      }
  }

  def initializePopulation(populationSize: Int) : Unit ={
    population = new ArrayBuffer[Bar]
    for(i <- 0 until populationSize){
      val pattern = new Pattern()

      pattern.setVoice(i)
      pattern.setInstrument("Piano")
      pattern.setTempo(tempo)

      for(j <- 0 until measureLength){
        // Generate notes between C4 and C6
        val note = new Note(48 + rng.nextInt(24), 0.125)
        pattern.add(note)
      }

      val indiv = getIndividualByPattern(pattern)
      population += indiv
    }
  }

  def getIndividualByPattern(pattern: Pattern) : Bar = {
  }

  def convertToPattern(bar: Bar) : Pattern = {

  }
}
