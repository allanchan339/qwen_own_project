import { useQuery } from '@tanstack/react-query'
import { graphApi } from '../lib/api'

export function useGraphStats() {
  return useQuery({
    queryKey: ['graph-stats'],
    queryFn: graphApi.getStats,
  })
}

export function useNodes(limit: number = 100) {
  return useQuery({
    queryKey: ['nodes', limit],
    queryFn: () => graphApi.getNodes(limit),
  })
}

export function useEdges(limit: number = 100) {
  return useQuery({
    queryKey: ['edges', limit],
    queryFn: () => graphApi.getEdges(limit),
  })
}

export function useCommunities() {
  return useQuery({
    queryKey: ['communities'],
    queryFn: graphApi.getCommunities,
  })
}

export function useGodNodes(topK: number = 10) {
  return useQuery({
    queryKey: ['god-nodes', topK],
    queryFn: () => graphApi.getGodNodes(topK),
  })
}

export function useNodeNeighbors(nodeId: string, maxDepth: number = 3) {
  return useQuery({
    queryKey: ['node-neighbors', nodeId, maxDepth],
    queryFn: () => graphApi.getNodeNeighbors(nodeId, maxDepth),
    enabled: !!nodeId,
  })
}

export function useReport() {
  return useQuery({
    queryKey: ['report'],
    queryFn: graphApi.getReport,
  })
}
