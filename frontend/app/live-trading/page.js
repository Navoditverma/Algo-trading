// app/live-trading/page.js
'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'

export default function LiveTradingPage() {
  const [strategies, setStrategies] = useState([])
  const [selectedStrategy, setSelectedStrategy] = useState('')
  const [isTrading, setIsTrading] = useState(false)
  const [pnl, setPnl] = useState(0)
  const [symbol,setSymbol]=useState('')
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/strategies/list`)
      .then((res) => {
        // Convert list of names to objects with id + name
        const formatted = res.data.map((item, index) => ({
          id: typeof item === 'string' ? item : item.id || `strategy-${index}`,
          name: typeof item === 'string' ? item : item.name || `Strategy ${index + 1}`
        }));        
        setStrategies(formatted);
      })
      .catch((err) => console.error('Failed to fetch strategies', err));
  }, []);
  

  const startTrading = async () => {
    try {
      setLogs([]); 
      setLogs((prev) => [...prev, `Analyzing chart for ${symbol} using ${selectedStrategy} strategy...`]);
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/trading/start?symbol=${symbol}&strategy_name=${selectedStrategy}`)
      setIsTrading(true)
      setLogs((prev) => [...prev, `Placing order for ${symbol}`]);

    } catch (err) {
      alert('Failed to start trading.')
    }
  }

  const stopTrading = async () => {
    try {
      await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/trading/stop?strategy_name=${selectedStrategy}`);
      setIsTrading(false);
    } catch (err) {
      alert('Failed to stop trading.');
      console.error(err);
    }
  }
  

  // Simulate fetching logs and PnL
  // useEffect(() => {
  //   if (!isTrading || !selectedStrategy) return;
  
  //   const interval = setInterval(async () => {
  //     try {
  //       const res = await axios.get(`http://localhost:8000/strategies/stats/${selectedStrategy}`);
  //       setPnl(res.data.pnl || 0);
  
  //       // Optional: Append to logs or simulate log entries here if needed
  //     } catch (err) {
  //       console.error("Failed to fetch strategy stats", err);
  //     }
  //   }, 3000);
  
  //   return () => clearInterval(interval);
  // }, [isTrading, selectedStrategy]);
  
  // useEffect(() => {
  //   if (!isTrading || !selectedStrategy) return;
  
  //   const interval = setInterval(async () => {
  //     try {
  //       const res = await axios.get(`http://localhost:8000/trading/live/logs?strategy_name=${selectedStrategy}`);
  //       setLogs(res.data.logs);
  //       setPnl(res.data.pnl);
  //     } catch (err) {
  //       console.error('Error fetching live logs:', err);
  //     }
  //   }, 3000);
  
  //   return () => clearInterval(interval);
  // }, [isTrading, selectedStrategy]);
  

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Live Trading</h1>

      <select
        className="border p-2 rounded w-full mb-4"
        value={selectedStrategy}
        onChange={(e) => setSelectedStrategy(e.target.value)}
        disabled={isTrading}
      >
        <option value="">Select Strategy</option>
        {strategies.map((s) => (
          <option key={s.id} value={s.id}>{s.name}</option>
        ))}
      </select>
      <input
          type="text"
          className="border p-2 rounded w-full mb-5"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Symbol (e.g. BTC or ETH)"
        />

      {!isTrading ? (
        <button
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          onClick={startTrading}
          disabled={!selectedStrategy}
        >
          Start Live Trading
        </button>
      ) : (
        <button
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          onClick={stopTrading}
        >
          Stop Trading
        </button>
      )}

      <div className="mt-6 p-4 bg-gray-50 border rounded">
        <h2 className="font-bold text-lg mb-2">Live Logs</h2>
        <div className="h-48 overflow-y-auto bg-black text-green-400 p-2 rounded border border-green-600 font-mono">
          {logs.length === 0 ? (
            <p className="text-sm text-gray-500">No trades yet...</p>
          ) : (
            logs.map((log, idx) => (
              <p key={idx} className="text-sm">{log}</p>
            ))
          )}
        </div>

        <button
          onClick={() => setLogs([])}
          className="mt-2 px-3 py-1 text-sm   border border-green-600 rounded"
        >
          Clear Logs
        </button>

        <div className="mt-4 font-semibold">
          Current PnL: <span className={pnl >= 0 ? 'text-green-600' : 'text-red-600'}>${pnl.toFixed(2)}</span>
        </div>
      </div>
    </div>
  )
}
