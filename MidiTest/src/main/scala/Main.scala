import csv.MatrixReader
import services.Initialisation

object Main {

  def main(args: Array[String]) : Unit = {
    val alg = new GeneticAlgorithm()
    alg.jfugueTest()
  }
}
