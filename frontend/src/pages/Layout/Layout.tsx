import { Outlet } from "react-router-dom";

function Layout() {

    return (
        <div className="bg-cover grid grid-cols-1 overflow-hidden place-items-stretch bg-white gap-2">
            <div className="flex justify-center items-center bg-blue-400 rounded-box pt-10 pb-10">
                <div className="w-400 min-h-200 flex justify-center">
                    <Outlet />
                </div>
            </div>
        </div>
    )
}

export default Layout;
