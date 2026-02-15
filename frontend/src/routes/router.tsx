import { createBrowserRouter } from "react-router-dom";
import HomePage from "../pages/Homepage";
import UploadPage from "../pages/UploadPage";
import JobListPage from "../pages/JobListPage";
import VideoPage from "../pages/VideoPage";
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
      {
        path: "/upload",
        element: <UploadPage />,
      },
      {
        path: "/joblist",
        element: <JobListPage />,
      },
      {
        path: "/video/:id",
        element: <VideoPage />,
      },
    ],
  },
]);

export default router
