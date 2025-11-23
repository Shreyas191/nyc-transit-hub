// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// 导入你的路由组件（关键！）
import AppRouter from './routes';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <AppRouter /> {/* 这里是你的路由，不是默认的<App /> */}
  </React.StrictMode>
);