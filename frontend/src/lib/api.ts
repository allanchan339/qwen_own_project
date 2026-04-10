import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface GraphStats {
  nodes: number
  edges: number
  communities: number
  average_degree: number
  density: number
}

export interface Node {
  id: string
  label: string
  file_type: string
  source_file: string
  source_location: string | null
  degree: number
}

export interface Edge {
  source: string
  target: string
  relation: string
  confidence: string
  confidence_score: number
  weight: number
}

export interface Community {
  id: number
  label: string
  nodes: string[]
  cohesion: number
}

export interface GodNode {
  node_id: string
  label: string
  degree: number
  betweenness: number
}

export interface PathResult {
  from_node: string
  to_node: string
  path: string[]
  hops: number
  relations: string[]
}

export const graphApi = {
  getStats: async (): Promise<GraphStats> => {
    const response = await api.get<GraphStats>('/graph/stats')
    return response.data
  },

  getNodes: async (limit: number = 100): Promise<Node[]> => {
    const response = await api.get<Node[]>('/graph/nodes', { params: { limit } })
    return response.data
  },

  getEdges: async (limit: number = 100): Promise<Edge[]> => {
    const response = await api.get<Edge[]>('/graph/edges', { params: { limit } })
    return response.data
  },

  getCommunities: async (): Promise<Community[]> => {
    const response = await api.get<Community[]>('/graph/communities')
    return response.data
  },

  getGodNodes: async (topK: number = 10): Promise<GodNode[]> => {
    const response = await api.get<GodNode[]>('/graph/god-nodes', { params: { top_k: topK } })
    return response.data
  },

  getNodeNeighbors: async (nodeId: string, maxDepth: number = 3): Promise<any> => {
    const response = await api.get(`/graph/node/${nodeId}/neighbors`, { params: { max_depth: maxDepth } })
    return response.data
  },

  findPath: async (fromNode: string, toNode: string): Promise<PathResult> => {
    const response = await api.get<PathResult>('/graph/path', { params: { from_node: fromNode, to_node: toNode } })
    return response.data
  },

  getReport: async (): Promise<{ report: string }> => {
    const response = await api.get('/graph/report')
    return response.data
  },
}

export default api
