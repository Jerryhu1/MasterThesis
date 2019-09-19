package csv

import models.{Matrix, Note}
import models.Matrix.Matrix

import scala.collection.mutable
import scala.io.Source

object MatrixReader {

  val fileName = "transition-matrix.csv"

  def getTransitionMatrixFromFile: Matrix = {
    val dir = System.getProperty("user.dir")
    val src = Source.fromFile(dir + "/resources/" + fileName)
    val lines = src.getLines()
    val notes = lines.next().split(",").drop(1).map(_.replaceAll("\"", ""))
    val iterator = lines.map(_.split(","))

    val matrix = new mutable.HashMap[(Note, Note), Double]

    // for each row in csv
    iterator foreach(row => {
      // for each note horizontally
      notes.zipWithIndex.foreach { case (note, i) =>
        // Replace quotes the vertical axis note
        val currNote = row(0).replaceAll("\"", "")
        val p = row(i+1)
        val transition = (Note.fromNoteString(currNote, 0.25), Note.fromNoteString(note, 0.25))
        matrix += (transition -> p.toDouble)
      }
    })
    return matrix
  }

}
