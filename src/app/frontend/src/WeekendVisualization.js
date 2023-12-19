import React, { useState, useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import axios from 'axios'

const PovertyVisualization = () => {
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
            let endpoint = 'http://172.25.0.3:8000/incidents/weekend/'
            const params = {}

            if (selectedState) {
                params.state = selectedState
            }

            if (selectedYear) {
                params.year = selectedYear
            }

            const response = await axios.get(endpoint, { params })
            const jsonData = response.data

            const uniqueStates = Array.from(
                new Set(jsonData.map((entry) => entry.state))
            )
            const uniqueYears = Array.from(
                new Set(jsonData.map((entry) => entry.year))
            )

            setStates(uniqueStates)
            setYears(uniqueYears)
            setData(jsonData)
            setChartUpdated(true)
        } catch (error) {
            console.error('Error fetching data:', error)
        }
    }

    const updateChart = () => {
        const labels = Array.from(
            new Set(data.map((entry) => `${entry.year} - ${entry.state}`))
        )
        const nIncidentsNoWeekend = data
            .filter((entry) => entry.is_weekend === 0)
            .map((entry) => entry.n_incidents_per_day)
        const nIncidentsWeekend = data
            .filter((entry) => entry.is_weekend === 1)
            .map((entry) => entry.n_incidents_per_day)

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
                        label: 'Incidentes / 100,000 habitantes y día en día de semana',
                        data: nIncidentsNoWeekend,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        order: 1,
                    },
                    {
                        label: 'Incidentes / 100,000 habitantes y día en fin de semana',
                        data: nIncidentsWeekend,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        order: 2,
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
            <h1>Pobreza</h1>

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

            <label htmlFor="year">Año:</label>
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
                id="povertyChart"
                width="800"
                height="400"
                ref={chartRef}
            ></canvas>
        </div>
    )
}

export default PovertyVisualization
