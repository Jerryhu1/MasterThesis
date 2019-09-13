import csv.MatrixReader
import services.Initialisation

object Main {

  def main(args: Array[String]) : Unit = {
    //val alg = new GeneticAlgorithm(1000, 1000)
    //alg.run()
    val matrix = MatrixReader.getTransitionMatrixFromFile()
    Initialisation.initializePopulationByModel(matrix, 10)
  }
}
