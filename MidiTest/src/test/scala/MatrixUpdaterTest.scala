import models.Matrix.Matrix
import models.{Bar, Note}
import org.scalatest.FunSuite
import services.MatrixUpdater

import scala.collection.mutable
import scala.collection.mutable.{ArrayBuffer, ListBuffer}

class MatrixUpdaterTest extends FunSuite{

    test("MatrixUpdater frequency vector should return correct count of each note") {
        val allNotes = population.flatMap(_.notes)

        val freqVector = MatrixUpdater.createFrequencyVector(allNotes)

        assert(freqVector("A") == 8)
        assert(freqVector("B") == 5)
        assert(freqVector("C") == 3)
        assert(freqVector("D") == 1)
        assert(freqVector("E") == 3)
    }

    test("MatrixUpdater should create a frequency matrix with counts equal to frequency vector"){
        val allNotes = population.flatMap(_.notes)
        val freqVector = MatrixUpdater.createFrequencyVector(allNotes)
        val freqMatrix = MatrixUpdater.createFrequencyMatrix(allNotes, freqVector)

        val t = freqMatrix.filter(item => "A".equals(item._1._1.name))
        val count = t.foldLeft(0.0)((acc, i) => acc + i._2)

        assert(count == 8.0)


    }

    test("Probabilities of frequency matrix should add up to one after division by frequency vector") {
        val allNotes = population.flatMap(_.notes)
        val freqVector = MatrixUpdater.createFrequencyVector(allNotes)
        val freqMatrix = MatrixUpdater.createFrequencyMatrix(allNotes, freqVector)

        val pMatrix = freqMatrix.collect{ case (k,v) => (k, v / freqVector(k._1.name)) }
        val pA = pMatrix.filter(item => "A".equals(item._1._1.name))
        val sumA = pA.foldLeft(0.0)((acc, i) => acc + i._2)
        val pB = pMatrix.filter(item => "B".equals(item._1._1.name))
        val sumB = pB.foldLeft(0.0)((acc, i) => acc + i._2)
        assert(sumA == 1.0)
        assert(sumB == 1.0)
    }

    test("Error matrix should correctly be instantiated by taking the difference") {
        val allNotes = population.flatMap(_.notes)

        val freqVector = MatrixUpdater.createFrequencyVector(allNotes)
        val tMatrix = MatrixUpdater.createFrequencyMatrix(allNotes, freqVector)

        val pMatrix = tMatrix.collect{ case (k,v) => (k, v / freqVector(k._1.name)) }

        // Create error matrix by taking the difference of initial and current matrix
        val errorMatrix = matrix.map {
            case (k, v) if pMatrix.contains(k) => (k, pMatrix(k) - v)
            case (k, v) => (k, -v)
        }



    }

    lazy val matrix : Matrix = mutable.Map[(Note, Note), Double](
        (A,A) -> 0.2,(A,B) -> 0.2, (A,C) -> 0.2,(A,D) -> 0.2,(A,E) -> 0.2,
        (B,A) -> 0.2,(B,B) -> 0.2, (B,C) -> 0.2,(B,D) -> 0.2,(B,E) -> 0.2,
        (C,A) -> 0.2,(C,B) -> 0.2, (C,C) -> 0.2,(C,D) -> 0.2,(C,E) -> 0.2,
        (D,A) -> 0.2,(D,B) -> 0.2, (D,C) -> 0.2,(D,D) -> 0.2,(D,E) -> 0.2,
        (E,A) -> 0.2,(E,B) -> 0.2, (E,C) -> 0.2,(E,D) -> 0.2,(E,E) -> 0.2,
    )

    val A = new Note(1, 0.25, "A")
    val B = new Note(1, 0.25, "B")
    val C = new Note(1, 0.25, "C")
    val D = new Note(1, 0.25, "D")
    val E = new Note(1, 0.25, "E")
    val X = new Note(1, 0.25, "X")

    val population : ArrayBuffer[Bar] = ArrayBuffer[Bar](
        new Bar(
            ListBuffer(A, A, A ,B)
        ),
        new Bar(
            ListBuffer(C, A, B, B)
        ),
        new Bar(
            ListBuffer(C, C, A, A)
        ),
        new Bar(
            ListBuffer(D, E, E, E)
        ),
        new Bar(
            ListBuffer(A, B, A, B)
        )
    )
}
