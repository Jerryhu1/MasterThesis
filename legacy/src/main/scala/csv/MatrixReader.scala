package csv

import models.Note
import models.Matrix.Matrix
import services.Duration

import scala.collection.mutable
import scala.io.Source
import scala.util.Try

object MatrixReader {

  val fileName = "transition-matrix.csv"

  def getEmptyMatrix: Matrix = {
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
        //TODO: Change duration to actual from corpus
        val transition = (Note.fromNoteString(note, Duration.getDuration()), Note.fromNoteString(currNote, Duration.getDuration()))
        matrix += (transition -> 0.0)
      })
    }
    matrix
  }

  def getEmptyFrequencyVector: mutable.HashMap[Note, Int] = {
    val dir = System.getProperty("user.dir")
    val src = Source.fromFile(dir + "/resources/" + fileName)
    val lines = src.getLines()
    val notes = lines.next().split(",").drop(1).map(_.replaceAll("\"", ""))
    val iterator = lines.map(_.split(",")).toList

    val vector = new mutable.HashMap[Note, Int]

    // for each note (column)
    notes.zipWithIndex.foreach { case (note, i) =>
      val n = Note.fromNoteString(note, Duration.getDuration())
      vector += (n -> 0)
    }

    vector
  }

  def getTransitionMatrixFromFile: Matrix = {
    val dir = System.getProperty("user.dir")
    val src = Source.fromFile(dir + "/resources/" + fileName)
    val lines = src.getLines()
    val notes = lines.next().split(",").drop(1).map(_.replaceAll("\"", ""))
    val iterator = lines.map(_.split(",")).toList

    val matrix = new mutable.HashMap[(Note, Note), Double]

      // for each note (column)
      notes.zipWithIndex.foreach { case (note, i) =>
        // for each row in csv
        iterator foreach (row => {
          // Replace quotes the vertical axis note
          val currNote = row(0).replaceAll("\"", "")
          val p = Try(row(i + 1).toDouble).toOption
          //TODO: Change duration to actual from corpus
          val transition = (Note.fromNoteString(note, Duration.getDuration()), Note.fromNoteString(currNote, Duration.getDuration()))
          p match {
            case None =>
              System.err.println(s"Could not parse probability value of transition $note -> $currNote, setting p to 0.0")
              matrix += (transition -> 0.0)
            case Some(v) => matrix += (transition -> v)
          }
        })

      }

    return matrix
  }

}
