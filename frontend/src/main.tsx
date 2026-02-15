import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './main.css'
import { RouterProvider } from 'react-router-dom'
import router from './routes/router'

createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
        <RouterProvider router={router} />
  </StrictMode>
)
