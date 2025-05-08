'use client';
import { useEffect, useState } from 'react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/history/backtests'); // Update if needed
        const data = await res.json();
        if (!Array.isArray(data)) {
          throw new Error("Expected array but got: " + JSON.stringify(data));
        }
    
        setHistory(data.reverse());  // Reverse only if it's an array
      } catch (err) {
        console.error('Error fetching history:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Backtest History</h1>
      {loading ? (
        <p>Loading...</p>
      ) : history.length === 0 ? (
        <p>No history found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 shadow">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 border">Date</th>
                <th className="px-4 py-2 border">Symbol</th>
                <th className="px-4 py-2 border">Strategy</th>
                <th className="px-4 py-2 border">Period</th>
                <th className="px-4 py-2 border">Final Balance</th>
              </tr>
            </thead>
            <tbody>
              {history.map((entry, index) => (
                <tr key={index} className="text-center">
                  <td className="px-4 py-2 border">{new Date(entry.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-2 border">{entry.symbol}</td>
                  <td className="px-4 py-2 border">{entry.strategy}</td>
                  <td className="px-4 py-2 border">{entry.start_date} → {entry.end_date}</td>
                  <td className="px-4 py-2 border">${entry.final_balance.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
