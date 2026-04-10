import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import GraphView from './pages/GraphView'
import Communities from './pages/Communities'
import Report from './pages/Report'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="graph" element={<GraphView />} />
        <Route path="communities" element={<Communities />} />
        <Route path="report" element={<Report />} />
      </Route>
    </Routes>
  )
}

export default App
