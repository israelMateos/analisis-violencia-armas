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
            <div>
                <button onClick={() => handleTabChange('climate')}>
                    Clima
                </button>
                <button onClick={() => handleTabChange('firearmLaws')}>
                    Leyes
                </button>
                <button onClick={() => handleTabChange('poverty')}>
                    Pobreza
                </button>
                <button onClick={() => handleTabChange('weekend')}>
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
