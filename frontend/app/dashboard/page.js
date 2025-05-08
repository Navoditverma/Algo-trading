// app/(pages)/dashboard/page.js
import React from 'react';
import Portfolio from '../components/Portfolio';
import RecentTrades from '../components/RecentTrades';
import StrategyPerformance from '../components/StrategyPerformance';

export default function DashboardPage() {
  return (
    <div className="p-6 space-y-8">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <Portfolio />
      <RecentTrades />
      <StrategyPerformance />
    </div>
  );
}
