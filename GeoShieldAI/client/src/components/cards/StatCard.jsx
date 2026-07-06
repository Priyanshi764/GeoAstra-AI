import { Outlet } from "react-router-dom";

import Sidebar from "../components/sidebar/Sidebar";
import Navbar from "../components/navbar/Navbar";

export default function MainLayout() {

  return (

    <div className="flex h-screen bg-[#0B1220] text-white">

      <Sidebar />

      <div className="flex-1 flex flex-col">

        <Navbar />

        <main className="flex-1 overflow-auto p-6">

          <Outlet />

        </main>

      </div>

    </div>

  );

}