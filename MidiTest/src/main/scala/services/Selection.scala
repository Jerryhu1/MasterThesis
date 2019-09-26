package services

import models.Bar

import scala.collection.mutable.ArrayBuffer

object Selection {

    def tournament(population: ArrayBuffer[Bar]) : ArrayBuffer[Bar] = {
        var selectedPopulation = new ArrayBuffer[Bar]
        if(population.length % 4 > 0){
            System.err.println("Population can not be divided by 4!, specify a different tournament- or population size")
        }
        for(i <- population.indices by 4) {
            val selectedIndividuals : ArrayBuffer[Bar] = population.slice(i, i + 4).sortBy(x => x.fitness).take(2)
            selectedPopulation ++= selectedIndividuals
        }

        return selectedPopulation
    }
}
