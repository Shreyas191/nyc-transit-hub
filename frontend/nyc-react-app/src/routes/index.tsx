// src/routes/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Layout from '../components/layout/Layout';

const Home = () => <div style={{ padding: 20 }}>这是我的首页！</div>;

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />, 
    children: [
      { path: '/', element: <Home /> }, 
    ],
  },
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}