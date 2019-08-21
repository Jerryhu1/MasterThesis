package services

import Rng.rng

object Duration {

  def getDuration(): Double = {
    val durationCase = rng.nextInt(10)
    if(durationCase < 6){
      return 0.250
    }
    if(durationCase < 8){
      0.5
    }
    else{
      0.125
    }
  }
}
