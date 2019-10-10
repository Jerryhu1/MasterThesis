package constants

import models.Bar
import models.Matrix.Matrix
import services._

import scala.collection.mutable.ArrayBuffer

object Constants {

  val filePath = "./resources/transition-matrix.csv"
  // EA
  val populationSize = 100
  lazy val samplePopulationSize: Int = 10
  lazy val crossoverPopulationSize: Int = 10
  val iterations = 10
  val learningRate = 0.1 // Rate the model gets updated by selection
    // Operators
  val crossover: (Bar, Bar) => (Bar, Bar) = (c1: Bar, c2: Bar) => Crossover.onePoint(c1, c2)
  val initialisation: (Matrix, Int) => ArrayBuffer[Bar] = (m: Matrix, n: Int) => Initialisation.initializePopulationByModel(m, n)
  val mutation: Bar => Unit = (b: Bar) => Mutation.changePitch(b)
  val fitnessFunction: Bar => Double = (b: Bar) => Fitness.getFitness(b)
  val selection: ArrayBuffer[Bar] => ArrayBuffer[Bar] = (p: ArrayBuffer[Bar]) => Selection.tournament(p)

  // Music
  lazy val measureLength: Int = bars * durationUnit // # Notes total
  val bars = 4
  val durationUnit = 8 // 8th note, 16th note
  val tempo = 120 // BPM
  //Note range
  val minNote = 64
  val maxNote = 74

  object Duration {
    val whole : Double = 1.0
    val half : Double = 0.5
    val fourth : Double = 0.25
    val eight : Double = 0.125
    val sixteenth : Double = 0.125 / 2
    val eightTriplet: Double = 0.25 / 3
  }
}
