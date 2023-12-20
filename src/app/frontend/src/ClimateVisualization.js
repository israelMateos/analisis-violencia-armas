import React, { useState, useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import axios from 'axios'

const ClimateVisualization = () => {
    const [data, setData] = useState([])
    const [states, setStates] = useState([])
    const [years, setYears] = useState([])
    const [selectedState, setSelectedState] = useState('')
    const [selectedYear, setSelectedYear] = useState('')
    const [chartUpdated, setChartUpdated] = useState(false)
    const chartRef = useRef(null)

    useEffect(() => {
        fetchData()
    }, [selectedState, selectedYear])

    useEffect(() => {
        if (chartUpdated) {
            updateChart()
            setChartUpdated(false)
        }
    }, [data, chartUpdated])

    const fetchData = async () => {
        try {
            let endpoint = `http://localhost:8000/incidents/climate/`
            console.log('Backend Host:', process.env.BACKEND_HOST);
            const params = {}

            if (selectedState) {
                params.state = selectedState
            }

            if (selectedYear) {
                params.year = selectedYear
            }

            const response = await axios.get(endpoint, { params })
            const jsonData = response.data

            const groupedData = jsonData.reduce((acc, entry) => {
                const key = `${entry.year}_${entry.state}`
                if (!acc[key]) {
                    acc[key] = {
                        year: entry.year,
                        state: entry.state,
                        n_incidents: 0,
                        total_temperature: 0,
                        total_precipitation: 0,
                        count: 0,
                    }
                }

                acc[key].n_incidents += entry.n_incidents
                acc[key].total_temperature += entry.average_temperature
                acc[key].total_precipitation += entry.average_precipitation
                acc[key].count += 1

                return acc
            }, {})

            const meanData = Object.values(groupedData).map((group) => ({
                year: group.year,
                state: group.state,
                n_incidents: group.n_incidents / group.count,
                average_temperature: group.total_temperature / group.count,
                average_precipitation: group.total_precipitation / group.count,
            }))

            const uniqueStates = Array.from(
                new Set(meanData.map((entry) => entry.state))
            )
            const uniqueYears = Array.from(
                new Set(meanData.map((entry) => entry.year))
            )

            setStates(uniqueStates)
            setYears(uniqueYears)
            setData(meanData)
            setChartUpdated(true) // Signal that the data is ready for chart update
        } catch (error) {
            console.error('Error fetching data:', error)
        }
    }

    const updateChart = () => {
        const labels = data.map((entry) => `${entry.year} - ${entry.state}`)
        const nIncidents = data.map((entry) => entry.n_incidents)
        const avgTemperature = data.map((entry) => entry.average_temperature)
        const avgPrecipitation = data.map(
            (entry) => entry.average_precipitation
        )

        const ctx = chartRef.current

        if (window.myChart) {
            window.myChart.destroy()
        }

        window.myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        type: 'line',
                        label: 'Número de incidentes / 100.000 habitantes',
                        data: nIncidents,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        order: 1,
                    },
                    {
                        type: 'bar',
                        label: 'Temperatura media',
                        data: avgTemperature,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        order: 2,
                    },
                    {
                        type: 'bar',
                        label: 'Precipitaciones medias',
                        data: avgPrecipitation,
                        backgroundColor: 'rgba(255, 205, 86, 0.2)',
                        borderColor: 'rgba(255, 205, 86, 1)',
                        borderWidth: 1,
                        order: 3,
                    },
                ],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        })
    }

    return (
        <div>
            <h1>Clima</h1>

            <label htmlFor="state">Estado:</label>
            <select
                id="state"
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
            >
                <option value="">Todos los estados</option>
                {states.map((state) => (
                    <option key={state} value={state}>
                        {state}
                    </option>
                ))}
            </select>

            <label htmlFor="year">Año :</label>
            <select
                id="year"
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
            >
                <option value="">Todos los años</option>
                {years.map((year) => (
                    <option key={year} value={year}>
                        {year}
                    </option>
                ))}
            </select>

            <canvas
                id="barChart"
                width="800"
                height="400"
                ref={chartRef}
            ></canvas>
        </div>
    )
}

export default ClimateVisualization
