package models

case class Note(var note: Integer, var duration : Double) {
  def toJFugueNote(): org.jfugue.theory.Note = {
    new org.jfugue.theory.Note(note, duration)
  }

}
object Note{
  def fromNoteString(note: String, duration: Double) : Note = {
    val fugueNote = new org.jfugue.theory.Note(note)
    //TODO: Check what this returns
    Note(fugueNote.getValue.toInt, duration)
  }

}
