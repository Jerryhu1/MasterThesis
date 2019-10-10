package services

import constants.Constants
import csv.MatrixReader
import models.{Bar, Note}
import models.Matrix.Matrix

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

object MatrixUpdater {

  //TODO: Implement this
  def updateMatrix(individuals: ArrayBuffer[Bar], matrix: Matrix) : Matrix = {

    val freqVector = new mutable.HashMap[Note, Int]()
    val allNotes = individuals.flatMap(_.notes)
    val totalNotes = allNotes.length
    // Construct first-order frequency vector
    for (n <- allNotes){
      val v = freqVector.get(n)
      v match {
        case None => freqVector += (n -> 1)
        case Some(_) => freqVector.update(n, freqVector(n) + 1)
      }
    }

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

    // Divide each transition by the frequency of starting note to get probabilities
//    for((k,_) <- tMatrix){
//      tMatrix(k) = tMatrix(k) / freqVector(k._1)
//    }
    val pMatrix = tMatrix.collect{ case (k,v) => (k, v / freqVector(k._1)) }

    // Create error matrix by taking the difference of initial and current matrix
    val errorMatrix = matrix.map {
      case (k, v) if pMatrix.contains(k) => (k, pMatrix(k) - v)
      case (k, v) => (k, -v)
    }


    // Update the matrix by adding the error * learning rate to initial matrix values
    val updatedMatrix = matrix.collect{ case (k,v) => (k, v + (Constants.learningRate * errorMatrix(k)) ) }

    return updatedMatrix
  }
}
