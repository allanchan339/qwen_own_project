import { useEffect, useRef, useState } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { Search, ZoomIn, ZoomOut, Maximize } from 'lucide-react'
import { useNodes, useEdges, useNodeNeighbors } from '../hooks/useGraphData'
import { Node as NodeType } from '../lib/api'

function GraphView() {
  const { data: nodes = [] } = useNodes(500)
  const { data: edges = [] } = useEdges(500)
  const [selectedNode, setSelectedNode] = useState<NodeType | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<NodeType[]>([])
  const fgRef = useRef<any>(null)
  const { data: neighbors } = useNodeNeighbors(selectedNode?.id || '', 3)

  // Filter nodes based on search
  useEffect(() => {
    if (!searchQuery) {
      setSearchResults([])
      return
    }
    const filtered = nodes.filter(
      (node) =>
        node.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
        node.id.toLowerCase().includes(searchQuery.toLowerCase())
    )
    setSearchResults(filtered.slice(0, 10))
  }, [searchQuery, nodes])

  const handleNodeClick = (node: any) => {
    setSelectedNode(node)
    if (fgRef.current) {
      fgRef.current.centerAt(node.x, node.y, 1000)
    }
  }

  const handleResetView = () => {
    if (fgRef.current) {
      fgRef.current.camera({
        x: 0,
        y: 0,
        z: 1,
        duration: 1000,
      })
    }
    setSelectedNode(null)
  }

  const handleZoomIn = () => {
    if (fgRef.current) {
      const current = fgRef.current.camera()
      fgRef.current.camera({
        ...current,
        z: current.z * 0.8,
        duration: 300,
      })
    }
  }

  const handleZoomOut = () => {
    if (fgRef.current) {
      const current = fgRef.current.camera()
      fgRef.current.camera({
        ...current,
        z: current.z * 1.2,
        duration: 300,
      })
    }
  }

  // Color nodes based on degree
  const getNodeColor = (node: NodeType) => {
    const degree = node.degree || 0
    if (degree >= 10) return '#dc2626' // red
    if (degree >= 5) return '#f59e0b' // orange
    if (degree >= 3) return '#3b82f6' // blue
    return '#6b7280' // gray
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      {/* Graph Canvas */}
      <div className="flex-1 bg-white rounded-lg shadow-sm border border-gray-200 relative">
        <div className="absolute top-4 left-4 z-10 flex gap-2">
          <button
            onClick={handleZoomIn}
            className="btn btn-secondary p-2"
            title="Zoom In"
          >
            <ZoomIn className="w-5 h-5" />
          </button>
          <button
            onClick={handleZoomOut}
            className="btn btn-secondary p-2"
            title="Zoom Out"
          >
            <ZoomOut className="w-5 h-5" />
          </button>
          <button
            onClick={handleResetView}
            className="btn btn-secondary p-2"
            title="Reset View"
          >
            <Maximize className="w-5 h-5" />
          </button>
        </div>

        <ForceGraph2D
          ref={fgRef}
          graphData={{
            nodes: nodes.map((n) => ({
              id: n.id,
              label: n.label,
              vx: 0,
              vy: 0,
              file_type: n.file_type,
              degree: n.degree,
            })) as any,
            links: edges.map((e) => ({
              source: e.source,
              target: e.target,
            })) as any,
          }}
          nodeLabel="label"
          nodeColor={getNodeColor}
          nodeRelSize={6}
          nodeVal={3}
          linkColor={() => '#9ca3af'}
          linkWidth={1}
          onNodeClick={handleNodeClick}
          backgroundColor="transparent"
          width={document.querySelector('.graph-container')?.clientWidth || 800}
          height={document.querySelector('.graph-container')?.clientHeight || 600}
        />
      </div>

      {/* Sidebar */}
      <div className="w-80 flex flex-col gap-4">
        {/* Search */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search nodes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          {searchResults.length > 0 && (
            <div className="mt-2 max-h-48 overflow-y-auto">
              {searchResults.map((node) => (
                <button
                  key={node.id}
                  onClick={() => {
                    handleNodeClick(node)
                    setSearchQuery('')
                    setSearchResults([])
                  }}
                  className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <p className="font-medium text-sm text-gray-900">{node.label}</p>
                  <p className="text-xs text-gray-500">{node.id}</p>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Selected Node Info */}
        {selectedNode && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <h3 className="font-semibold text-gray-900 mb-3">Node Details</h3>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-500">Label</p>
                <p className="font-medium text-gray-900">{selectedNode.label}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">ID</p>
                <p className="font-mono text-xs text-gray-900 break-all">{selectedNode.id}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Type</p>
                <p className="font-medium text-gray-900">{selectedNode.file_type}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Connections</p>
                <p className="font-medium text-gray-900">{selectedNode.degree}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Source</p>
                <p className="font-mono text-xs text-gray-900 break-all">{selectedNode.source_file}</p>
              </div>
            </div>

            {neighbors && neighbors.nodes && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm font-medium text-gray-700 mb-2">
                  Connected Nodes ({neighbors.nodes.length})
                </p>
                <div className="max-h-48 overflow-y-auto space-y-1">
                  {neighbors.nodes.map((n: any) => (
                    <button
                      key={n.id}
                      onClick={() => handleNodeClick(n)}
                      className="w-full text-left px-2 py-1.5 text-sm hover:bg-gray-50 rounded transition-colors"
                    >
                      <p className="font-medium text-gray-900">{n.label}</p>
                      <p className="text-xs text-gray-500">Depth: {n.depth}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Legend */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 className="font-semibold text-gray-900 mb-3">Node Color Legend</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-red-600"></div>
              <span className="text-sm text-gray-600">10+ connections</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-amber-500"></div>
              <span className="text-sm text-gray-600">5-9 connections</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-blue-500"></div>
              <span className="text-sm text-gray-600">3-4 connections</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-gray-500"></div>
              <span className="text-sm text-gray-600">1-2 connections</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GraphView
