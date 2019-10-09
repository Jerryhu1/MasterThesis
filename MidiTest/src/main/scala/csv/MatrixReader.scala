package csv

import models.Note
import models.Matrix.Matrix
import services.Duration

import scala.collection.mutable
import scala.io.Source

object MatrixReader {

  val fileName = "transition-matrix.csv"

  def getTransitionMatrixFromFile: Matrix = {
    val dir = System.getProperty("user.dir")
    val src = Source.fromFile(dir + "/resources/" + fileName)
    val lines = src.getLines()
    val notes = lines.next().split(",").drop(1).map(_.replaceAll("\"", ""))
    val iterator = lines.map(_.split(",")).toList

    val matrix = new mutable.HashMap[(Note, Note), Double]

      // for each note (column)
      notes.zipWithIndex.foreach { case (note, i) =>
        print(note)
        // for each row in csv
        iterator foreach (row => {
          // Replace quotes the vertical axis note
          val currNote = row(0).replaceAll("\"", "")
          val p = row(i + 1)
          //TODO: Change duration to actual from corpus
          val transition = (Note.fromNoteString(note, Duration.getDuration()), Note.fromNoteString(currNote, Duration.getDuration()))
          matrix += (transition -> p.toDouble)
        })
      }

    return matrix
  }

}
