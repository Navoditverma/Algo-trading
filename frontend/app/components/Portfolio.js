export default function Portfolio() {
  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-xl font-medium mb-2">Portfolio Overview</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-gray-500">Total Equity</p>
          <p className="text-lg font-semibold">$10,000</p>
        </div>
        <div>
          <p className="text-gray-500">Open Positions</p>
          <p className="text-lg font-semibold">3</p>
        </div>
      </div>
    </div>
  );
}
