import { Layers, Users, Activity } from 'lucide-react'
import { useCommunities, useNodes } from '../hooks/useGraphData'

function Communities() {
  const { data: communities = [], isLoading } = useCommunities()
  const { data: nodes = [] } = useNodes(1000)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const getNodeCountByType = (nodeIds: string[]) => {
    const nodeMap = new Map(nodes.map((n) => [n.id, n.file_type]))
    const counts: Record<string, number> = {}
    
    nodeIds.forEach((id) => {
      const type = nodeMap.get(id) || 'unknown'
      counts[type] = (counts[type] || 0) + 1
    })
    
    return counts
  }

  const sortedCommunities = [...communities].sort((a, b) => b.nodes.length - a.nodes.length)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Communities</h1>
        <p className="text-gray-500 mt-1">
          Detected clusters of related concepts in the knowledge graph
        </p>
      </div>

      {/* Community Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {sortedCommunities.map((community) => {
          const typeCounts = getNodeCountByType(community.nodes)
          
          return (
            <div
              key={community.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
            >
              <div className="bg-gradient-to-r from-primary-500 to-primary-600 px-6 py-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-white">
                    {community.label}
                  </h2>
                  <span className="bg-white/20 text-white px-3 py-1 rounded-full text-sm font-medium">
                    {community.nodes.length} nodes
                  </span>
                </div>
              </div>

              <div className="p-6">
                {/* Cohesion Score */}
                <div className="mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-500 flex items-center gap-2">
                      <Activity className="w-4 h-4" />
                      Cohesion Score
                    </span>
                    <span className="font-semibold text-gray-900">
                      {(community.cohesion * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{ width: `${community.cohesion * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* Node Type Distribution */}
                <div className="mb-6">
                  <p className="text-sm text-gray-500 mb-2 flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    Node Types
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(typeCounts).map(([type, count]) => (
                      <span
                        key={type}
                        className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700"
                      >
                        {type}: {count}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Sample Nodes */}
                <div>
                  <p className="text-sm text-gray-500 mb-2">Sample Nodes</p>
                  <div className="space-y-1 max-h-32 overflow-y-auto">
                    {community.nodes.slice(0, 8).map((nodeId) => {
                      const node = nodes.find((n) => n.id === nodeId)
                      return (
                        <div
                          key={nodeId}
                          className="px-3 py-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                        >
                          <p className="text-sm font-medium text-gray-900">
                            {node?.label || nodeId}
                          </p>
                          {node && (
                            <p className="text-xs text-gray-500">{node.source_file}</p>
                          )}
                        </div>
                      )
                    })}
                  </div>
                  {community.nodes.length > 8 && (
                    <p className="text-xs text-gray-500 mt-2">
                      +{community.nodes.length - 8} more nodes
                    </p>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {communities.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Layers className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Communities Found</h3>
          <p className="text-gray-500">
            Run graphify extraction to detect communities in your codebase
          </p>
        </div>
      )}
    </div>
  )
}

export default Communities
