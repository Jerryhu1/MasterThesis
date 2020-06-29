package models

import scala.collection.mutable

object Matrix {

  type Matrix = mutable.Map[(Note, Note), Double] {

  }

}