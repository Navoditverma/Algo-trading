'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState([])

  useEffect(() => {
    fetchStrategies()
  }, [])

  const fetchStrategies = async () => {
    try {
      const  res = await (await fetch('http://127.0.0.1:8000/strategies/list')).json()
      console.log("Resule",res)
      setStrategies(res)
    } catch (error) {
      console.error('Error fetching strategies:', error)
    }
  }

  const handleCreateClick = () => {
    alert('🚧 Feature coming soon: Create Strategy')
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Strategies</h1>
        <button
          onClick={handleCreateClick}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Create Strategy
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
        {strategies.map((strategy, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 border border-gray-100"
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-1">
                {strategy.name}
              </h2>
              <p className="text-sm text-gray-500 mb-4">
                Created: {new Date(strategy.created_at).toLocaleString()}
              </p>

              <div className="space-y-2 text-sm text-gray-700">
                <p>
                  📈 <span className="font-medium">PnL:+4.2%</span>{" "}
                  <span className="text-green-600 font-semibold">{strategy.pnl}</span>
                </p>
                <p>
                  📊 <span className="font-medium">Sharpe Ratio:1.05</span>{" "}
                  <span className="text-blue-600 font-semibold">{strategy.sharpe}</span>
                </p>
                <p>
                  🧾 <span className="font-medium">Trades Executed:23</span>{" "}
                  {strategy.trades}
                </p>
              </div>
            </div>
          ))}
    </div>

    </div>
  )
}
