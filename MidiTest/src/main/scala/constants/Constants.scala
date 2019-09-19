package constants

import models.Bar
import models.Matrix.Matrix
import services.{Crossover, Fitness, Initialisation, Mutation}

import scala.collection.mutable.ArrayBuffer

object Constants {

  val filePath = "./resources/transition-matrix.csv"
  // EA
  val populationSize = 100
  val iterations = 10
    // Operators
  val crossover: (Bar, Bar) => (Bar, Bar) = (c1: Bar, c2: Bar) => Crossover.onePoint(c1, c2)
  val initialisation: (Matrix, Int) => ArrayBuffer[Bar] = (m: Matrix, n: Int) => Initialisation.initializePopulationByModel(m, n)
  val mutation: Bar => Unit = (b: Bar) => Mutation.changePitch(b)
  val fitnessFunction: Bar => Int = (b: Bar) => Fitness.getFitness(b)

  // Music
  lazy val measureLength: Int = bars * durationUnit // # Notes total
  val bars = 8
  val durationUnit = 8 // 8th note, 16th note
  val tempo = 120 // BPM
  //Note range
  val minNote = 64
  val maxNote = 74



}
