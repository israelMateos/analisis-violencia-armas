import React, { useState } from 'react'
import ClimateVisualization from './ClimateVisualization'
import FirearmLawsVisualization from './FirearmLawsVisualization'
import PovertyVisualization from './PovertyVisualization'
import WeekendVisualization from './WeekendVisualization'

const Dashboard = () => {
    const [activeTab, setActiveTab] = useState('climate') // Default to ClimateVisualization

    const handleTabChange = (tab) => {
        setActiveTab(tab)
    }

    return (
        <div>
            <div className='w3-bar w3-black'>
                <button
                className={`w3-bar-item w3-button tablink ${activeTab === 'climate' ? 'w3-red' : ''}`}
                onClick={() => handleTabChange('climate')}
                id='climate-tablink'
                >
                Clima
                </button>
                <button
                className={`w3-bar-item w3-button tablink ${activeTab === 'firearmLaws' ? 'w3-red' : ''}`}
                onClick={() => handleTabChange('firearmLaws')}
                id='firearmLaws-tablink'
                >
                Leyes
                </button>
                <button
                className={`w3-bar-item w3-button tablink ${activeTab === 'poverty' ? 'w3-red' : ''}`}
                onClick={() => handleTabChange('poverty')}
                id='poverty-tablink'
                >
                Pobreza
                </button>
                <button
                className={`w3-bar-item w3-button tablink ${activeTab === 'weekend' ? 'w3-red' : ''}`}
                onClick={() => handleTabChange('weekend')}
                id='weekend-tablink'
                >
                Fin de semana
                </button>
            </div>

            {activeTab === 'climate' && <ClimateVisualization />}
            {activeTab === 'firearmLaws' && <FirearmLawsVisualization />}
            {activeTab === 'poverty' && <PovertyVisualization />}
            {activeTab === 'weekend' && <WeekendVisualization />}
        </div>
    )
}

export default Dashboard
