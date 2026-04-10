import { FileText, Download } from 'lucide-react'
import { useReport } from '../hooks/useGraphData'

function Report() {
  const { data, isLoading, error } = useReport()

  const downloadReport = () => {
    if (!data?.report) return
    
    const blob = new Blob([data.report], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'graph-report.md'
    a.click()
    URL.revokeObjectURL(url)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Report Available</h3>
        <p className="text-gray-500">
          Run graphify extraction to generate an analysis report
        </p>
      </div>
    )
  }

  if (!data?.report) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Report Available</h3>
        <p className="text-gray-500">
          Run graphify extraction to generate an analysis report
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analysis Report</h1>
          <p className="text-gray-500 mt-1">
            Comprehensive knowledge graph analysis
          </p>
        </div>
        <button
          onClick={downloadReport}
          className="btn btn-primary flex items-center gap-2"
        >
          <Download className="w-5 h-5" />
          Download Report
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="prose prose-gray max-w-none p-8">
          <div
            className="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-6 rounded-lg overflow-x-auto"
            dangerouslySetInnerHTML={{ __html: data.report.replace(/\n/g, '<br />') }}
          />
        </div>
      </div>
    </div>
  )
}

export default Report
