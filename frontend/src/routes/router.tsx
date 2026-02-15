import { createBrowserRouter } from "react-router-dom";
import HomePage from "../pages/Homepage";
import Layout from "../pages/Layout/Layout";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    // errorElement: < />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
    ],
  },
]);

export default router
