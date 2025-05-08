"use client";
import { useEffect, useState } from "react";

export default function LogsPage() {
  const [logs, setLogs] = useState("");

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/logs/log`);
        const text = await res.text();
        setLogs(text);
      } catch (err) {
        console.error("Failed to fetch logs:", err);
        setLogs("[ERROR] Could not load logs.");
      }
    };

    fetchLogs();

    // Optional: Poll every 5 seconds
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Logs</h1>
      <div className="bg-black text-green-400 p-2 rounded h-64 overflow-y-scroll font-mono whitespace-pre-wrap">
        {logs}
      </div>
    </div>
  );
}
