// app/backtest/page.js
'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'

export default function BacktestPage() {
  const [strategies, setStrategies] = useState([])
  const [selectedStrategy, setSelectedStrategy] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [balance, setBalance] = useState(10000)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [symbol, setSymbol] = useState('');
  

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

  const runBacktest = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/backtest/run`, null, {
        params: {
          symbol,
          strategy_name: selectedStrategy,
          start_date: start,
          end_date: end,
        },
      });
      setResult(res.data);
    } catch (err) {
      alert('Backtest failed.');
      console.error(err);
    }
    setLoading(false);
  };
  

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Backtest Strategy</h1>

      <div className="space-y-4 mb-6">
        <select
          className="border p-2 rounded w-full"
          value={selectedStrategy}
          onChange={(e) => setSelectedStrategy(e.target.value)}
        >
          <option value="">Select Strategy</option>
          {strategies.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}

        </select>
        
        <input
          type="text"
          className="border p-2 rounded w-full"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Symbol (e.g. BTC or ETH)"
        />


        <input
          type="date"
          className="border p-2 rounded w-full"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />

        <input
          type="date"
          className="border p-2 rounded w-full"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />

        <input
          type="number"
          className="border p-2 rounded w-full"
          value={balance}
          onChange={(e) => setBalance(e.target.value)}
          placeholder="Initial Balance"
        />

        <button
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          onClick={runBacktest}
          disabled={loading || !selectedStrategy}
        >
          {loading ? 'Running...' : 'Run Backtest'}
        </button>
      </div>

      {result && (
        <div className="mt-8 p-4 border rounded bg-gray-50">
          <h2 className="font-bold text-lg">Backtest Result</h2>
          <p><strong>Final Balance:</strong> ${result.final_balance.toFixed(2)}</p>
          <p><strong>Total Trades:</strong> {result.trade_history.length}</p>
          <p><strong>Metrics:</strong></p>
          <ul className="list-disc list-inside">
            {Object.entries(result.performance_metrics).map(([k, v]) => (
              <li key={k}><strong>{k}:</strong> {v}</li>
            ))}
          </ul>
        </div>
      )}

    </div>
  )
}
