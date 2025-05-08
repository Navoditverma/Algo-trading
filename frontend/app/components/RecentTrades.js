export default function RecentTrades() {
  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-xl font-medium mb-2">Recent Trades</h2>
      <ul className="text-sm space-y-2">
        <li>✔️ Bought AAPL - 2 shares @ $150</li>
        <li>✔️ Sold TSLA - 1 share @ $800</li>
        <li>✔️ Bought ETH - 0.5 @ $1,900</li>
      </ul>
    </div>
  );
}
