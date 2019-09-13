package constants

object Constants {

  // EA
  val populationSize = 100
  val iterations = 10

  // Music
  lazy val measureLength: Int = bars * durationUnit // # Notes total
  val bars = 8
  val durationUnit = 8 // 8th note, 16th note
  val tempo = 120 // BPM
  //Note range
  val minNote = 64
  val maxNote = 74


}
