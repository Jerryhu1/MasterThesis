import java.lang.Exception

import javax.sound.midi._
import org.jfugue.player._

object Main {

  def main(args: Array[String]) = {
    val alg = new GeneticAlgorithm()
    alg.run(5, 1)

//    try{
//      val sequencer = MidiSystem.getSequencer()
//      sequencer.open()
//      var sequence = new Sequence(Sequence.PPQ, 4)
//      var track = sequence.createTrack()
//      for(i <- 0 to 12 by 4) {
//        val ev1 = makeEvent(144, 1, 48, 100, i).get
//        val ev2 = makeEvent(128, 1, 48, 100, i+2).get
//        track.add(ev1)
//        track.add(ev2)
//      }
//      sequencer.setSequence(sequence)
//      sequencer.setTempoInBPM(120)
//      sequencer.start()
//
//      while (true) {
//        if(!sequencer.isRunning){
//          sequencer.close()
//          System.exit(1)
//        }
//      }
//    }catch{
//      case e: Exception => Console.out.print("Fail")
//    }

  }

  def makeEvent(command: Int, channel: Int, note: Int,
               velocity: Int, tick: Int) : Option[MidiEvent] = {
    try {
      val message = new ShortMessage()
      message.setMessage(command, channel, note, velocity)

      Some(new MidiEvent(message, tick))
    }catch{
      case e: Exception =>
        Console.out.print(e)
        None
    }
  }

  def createSequence = {
    val player = new org.jfugue.player.Player()
    player.play("T120 V0 I[Piano] C5q D5q E5q F5q V1 I[Piano] CmajW")
  }
}
