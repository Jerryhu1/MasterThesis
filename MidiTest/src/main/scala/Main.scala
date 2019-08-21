import java.lang.Exception

import javax.sound.midi._
import org.jfugue.player._

object Main {

  def main(args: Array[String]) = {
    val alg = new GeneticAlgorithm(1000, 1000)
    alg.run()
  }
}
