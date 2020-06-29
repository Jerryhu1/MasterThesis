package models

case class Note(var note: Integer, var duration : Double, var name: String) {
  def toJFugueNote(): org.jfugue.theory.Note = {
    val note = new org.jfugue.theory.Note(name)
    note.setDuration(duration)
    note
  }

  override def equals(obj: scala.Any): Boolean = {
    obj match {
      case x: Note => return x.name == this.name
      case _ => return super.equals(obj)
    }
    false
  }
}

object Note{
  def fromNoteString(note: String, duration: Double) : Note = {
    val fugueNote = new org.jfugue.theory.Note(note)
    Note(fugueNote.getValue.toInt, duration, note)
  }

}
