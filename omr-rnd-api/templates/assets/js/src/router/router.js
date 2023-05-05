import { lazy, Suspense } from "react";
import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import SuspenseLoader from "./SuspenseLoader";
import OmrScan from "../pages/OmrScan";
import OmrResults from "../pages/OmrResults";
import Students from "../pages/Students";
import Classes from "../pages/Classes";
import Exam from "../pages/Exam";

const Loader = (Component) => (props) =>
  (
    <Suspense fallback={<SuspenseLoader />}>
      <Component {...props} />
    </Suspense>
  );

const Home = Loader(lazy(() => import("../pages/Home")));
// const Contact = Loader(lazy(() => import('../pages/contact/Contact')));

// Dashboards
const router = createBrowserRouter([
  // const router: RouteObject[] = [
  {
    path: "/",
    element: <App />,
    errorElement: <h1>Not found</h1>,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "/scan",
        element: <OmrScan />,
      },
      {
        path: "/results",
        element: <OmrResults />,
      },
      {
        path: "/students",
        element: <Students />,
      },
      {
        path: "/class",
        element: <Classes />,
      },
      {
        path: "/exams",
        element: <Exam />,
      },
    ],
  },
]);

export default router;
