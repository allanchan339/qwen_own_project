import { BarChart3, Network, Layers, TrendingUp, Zap } from 'lucide-react'
import { useGraphStats, useGodNodes } from '../hooks/useGraphData'

function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useGraphStats()
  const { data: godNodes, isLoading: nodesLoading } = useGodNodes(5)

  if (statsLoading || nodesLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const statsCards = [
    {
      label: 'Total Nodes',
      value: stats?.nodes || 0,
      icon: Network,
      color: 'bg-blue-500',
    },
    {
      label: 'Total Edges',
      value: stats?.edges || 0,
      icon: BarChart3,
      color: 'bg-purple-500',
    },
    {
      label: 'Communities',
      value: stats?.communities || 0,
      icon: Layers,
      color: 'bg-green-500',
    },
    {
      label: 'Avg Degree',
      value: stats?.average_degree?.toFixed(2) || '0.00',
      icon: TrendingUp,
      color: 'bg-orange-500',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Knowledge graph overview and insights</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((card) => {
          const Icon = card.icon
          return (
            <div key={card.label} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 font-medium">{card.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{card.value}</p>
                </div>
                <div className={`w-12 h-12 ${card.color} rounded-lg flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* God Nodes */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            Most Connected Nodes
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Key concepts that bridge multiple areas of the knowledge graph
          </p>
        </div>
        <div className="divide-y divide-gray-200">
          {godNodes?.map((node, index) => (
            <div key={node.node_id} className="p-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center font-semibold text-sm">
                    {index + 1}
                  </span>
                  <div>
                    <p className="font-medium text-gray-900">{node.label}</p>
                    <p className="text-sm text-gray-500">{node.node_id}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <p className="text-sm text-gray-500">Connections</p>
                    <p className="font-semibold text-gray-900">{node.degree}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-500">Betweenness</p>
                    <p className="font-semibold text-gray-900">{node.betweenness.toFixed(4)}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
