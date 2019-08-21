package models

import org.jfugue.pattern.Pattern

import scala.collection.mutable.{ListBuffer}

class Bar(val notes: ListBuffer[Note] = ListBuffer()) {
  var fitness : Int = 0

  def convertToPattern(voice: Int, instrument: String, tempo: Int) : Pattern = {
    var pattern = new Pattern()
    pattern.setInstrument(instrument)
    pattern.setVoice(voice)
    pattern.setTempo(tempo)
    for(note <- notes){
      pattern.add(note.toJFugueNote())
    }
    pattern
  }

}

object Bar{

}
