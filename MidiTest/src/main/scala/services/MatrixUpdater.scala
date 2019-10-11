package services

import constants.Constants
import models.{Bar, Note}
import models.Matrix.Matrix
import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

object MatrixUpdater {

  //TODO: Implement this
  def updateMatrix(individuals: ArrayBuffer[Bar], matrix: Matrix) : Matrix = {

    val allNotes = individuals.flatMap(_.notes)

    val freqVector = createFrequencyVector(allNotes)
    val tMatrix = createFrequencyMatrix(allNotes, freqVector)

    val pMatrix = tMatrix.collect{ case (k,v) => (k, v / freqVector(k._1.name)) }

    // Create error matrix by taking the difference of initial and current matrix
    val errorMatrix = matrix.map {
      case (k, v) if pMatrix.contains(k) => (k, pMatrix(k) - v)
      case (k, v) => (k, -v)
    }

    // Update the matrix by adding the error * learning rate to initial matrix values
    val updatedMatrix = matrix.collect{ case (k,v) => (k, v + (Constants.learningRate * errorMatrix(k)) ) }

//    val t2 = updatedMatrix.filter(item => "A6".equals(item._1._1.name))
//    val p2 = t2.foldLeft(0.0d)((acc, i) => acc + i._2)

    return updatedMatrix
  }

  def createFrequencyVector(allNotes : ArrayBuffer[Note]) : mutable.HashMap[String, Int] = {
    val freqVector = new mutable.HashMap[String, Int]()
    // Construct first-order frequency vector
    for (n <- allNotes.map(_.name)) {
      val v = freqVector.get(n)
      v match {
        case None => freqVector += (n -> 1)
        case Some(_) => freqVector.update(n, freqVector(n) + 1)
      }
    }
    freqVector
  }

  def createFrequencyMatrix(allNotes : ArrayBuffer[Note], freqVector : mutable.HashMap[String, Int]) = {
    // Construct frequency matrix
    val tMatrix = new mutable.HashMap[(Note, Note), Double]()

    for(n <- 1 until allNotes.size){
      val currNote = allNotes(n)
      val prevNote = allNotes(n-1)
      if(n == 0){
        // Catch initial note
      }
      val transition = (prevNote, currNote)
      val optTransition = tMatrix.get(transition)
      optTransition match {
        case None => tMatrix += (transition -> 1)
        case Some(_) => tMatrix(transition) = tMatrix(transition) + 1
      }
    }

    tMatrix
  }
}
