// app/dashboard/layout.js
import Navbar from '../components/Navbar';

export default function DashboardLayout({ children }) {
  return (
    <div>
      {/* <Navbar /> */}
      <main className="p-6">{children}</main>
    </div>
  );
}
