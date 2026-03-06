'use client'
import { useState } from 'react'

const API = 'http://localhost:8000'

type LogEntry = {
  time: string
  agent: string
  message: string
  type: 'info' | 'success' | 'error'
}

export default function Home() {
  const [task, setTask] = useState('')
  const [subtask, setSubtask] = useState('')
  const [pipeline, setPipeline] = useState('')
  const [loading, setLoading] = useState(false)
  const [log, setLog] = useState<LogEntry[]>([])
  const [plan, setPlan] = useState('')
  const [result, setResult] = useState('')
  const [pipelineResult, setPipelineResult] = useState<any>(null)

  function addLog(agent: string, message: string, type: LogEntry['type'] = 'info') {
    const time = new Date().toLocaleTimeString()
    setLog(prev => [...prev, { time, agent, message, type }])
  }

  async function submitTask() {
    if (!task.trim()) return
    setLoading(true)
    setPlan('')
    addLog('RELAY', `Task received: "${task}"`, 'info')
    addLog('SERAPH', 'Thinking...', 'info')
    try {
      const res = await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: task })
      })
      const data = await res.json()
      setPlan(data.plan)
      addLog('SERAPH', 'Plan created successfully!', 'success')
    } catch (e) {
      addLog('RELAY', 'Error connecting to API', 'error')
    }
    setLoading(false)
  }

  async function executeSubtask() {
    if (!subtask.trim()) return
    setLoading(true)
    setResult('')
    addLog('RELAY', `Subtask sent to Daedalus: "${subtask}"`, 'info')
    addLog('DAEDALUS', 'Selecting tool...', 'info')
    try {
      const res = await fetch(`${API}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subtask })
      })
      const data = await res.json()
      setResult(data.result)
      addLog('DAEDALUS', `Done: ${data.result}`, 'success')
    } catch (e) {
      addLog('RELAY', 'Error connecting to API', 'error')
    }
    setLoading(false)
  }

  async function runPipeline() {
    if (!pipeline.trim()) return
    setLoading(true)
    setPipelineResult(null)
    addLog('RELAY', `Full pipeline starting: "${pipeline}"`, 'info')
    addLog('SERAPH', 'Creating plan...', 'info')
    try {
      const res = await fetch(`${API}/pipeline`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: pipeline })
      })
      const data = await res.json()
      setPipelineResult(data)
      addLog('SERAPH', 'Plan complete. Handing off to Daedalus...', 'success')
      addLog('DAEDALUS', `Executed ${data.total_subtasks} subtasks`, 'success')
      addLog('RELAY', 'Pipeline complete!', 'success')
    } catch (e) {
      addLog('RELAY', 'Pipeline error', 'error')
    }
    setLoading(false)
  }

  const agentColors: Record<string, string> = {
    RELAY: '#888888',
    SERAPH: '#4fc3f7',
    DAEDALUS: '#81c784',
  }

  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: '40px 20px' }}>

      {/* Header */}
      <div style={{ marginBottom: 40 }}>
        <h1 style={{ fontSize: 32, fontWeight: 'bold', color: '#4fc3f7', margin: 0 }}>
          RELAY
        </h1>
        <p style={{ color: '#888', margin: '8px 0 0 0' }}>
          Multi-Agent Coordination Platform
        </p>
      </div>

      {/* Agent status */}
      <div style={{ display: 'flex', gap: 16, marginBottom: 40 }}>
        {['SERAPH — Strategic Planner', 'DAEDALUS — Technical Executor'].map((label) => (
          <div key={label} style={{
            flex: 1, padding: '12px 16px',
            backgroundColor: '#1e2130',
            borderRadius: 8,
            borderLeft: `4px solid ${label.includes('SERAPH') ? '#4fc3f7' : '#81c784'}`
          }}>
            <div style={{ fontSize: 12, color: '#888' }}>AGENT ONLINE</div>
            <div style={{ fontSize: 14, fontWeight: 'bold' }}>{label}</div>
          </div>
        ))}
      </div>

      {/* Task submission */}
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 16, color: '#4fc3f7', marginBottom: 12 }}>
          Submit Task → Seraph
        </h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            value={task}
            onChange={e => setTask(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && submitTask()}
            placeholder="Describe a task for Seraph to plan..."
            style={{
              flex: 1, padding: '10px 14px',
              backgroundColor: '#1e2130',
              border: '1px solid #333',
              borderRadius: 6, color: '#fff', fontSize: 14
            }}
          />
          <button
            onClick={submitTask}
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: loading ? '#333' : '#4fc3f7',
              color: loading ? '#888' : '#000',
              border: 'none', borderRadius: 6,
              fontWeight: 'bold', cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Working...' : 'Plan'}
          </button>
          <button
            onClick={() => { setTask(''); setPlan('') }}
            style={{
              padding: '10px 16px',
              backgroundColor: 'transparent',
              color: '#888',
              border: '1px solid #333',
              borderRadius: 6,
              cursor: 'pointer'
            }}
          >
            Clear
          </button>
        </div>
        {plan && (
          <div style={{
            marginTop: 16, padding: 16,
            backgroundColor: '#1e2130',
            borderRadius: 8, borderLeft: '4px solid #4fc3f7',
            fontSize: 13, lineHeight: 1.6,
            whiteSpace: 'pre-wrap', color: '#ccc'
          }}>
            {plan}
          </div>
        )}
      </div>

      {/* Subtask execution */}
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 16, color: '#81c784', marginBottom: 12 }}>
          Execute Subtask → Daedalus
        </h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            value={subtask}
            onChange={e => setSubtask(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && executeSubtask()}
            placeholder="Give Daedalus a subtask to execute..."
            style={{
              flex: 1, padding: '10px 14px',
              backgroundColor: '#1e2130',
              border: '1px solid #333',
              borderRadius: 6, color: '#fff', fontSize: 14
            }}
          />
          <button
            onClick={executeSubtask}
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: loading ? '#333' : '#81c784',
              color: loading ? '#888' : '#000',
              border: 'none', borderRadius: 6,
              fontWeight: 'bold', cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Working...' : 'Execute'}
          </button>
          <button
            onClick={() => { setSubtask(''); setResult('') }}
            style={{
              padding: '10px 16px',
              backgroundColor: 'transparent',
              color: '#888',
              border: '1px solid #333',
              borderRadius: 6,
              cursor: 'pointer'
            }}
          >
            Clear
          </button>
        </div>
        {result && (
          <div style={{
            marginTop: 16, padding: 16,
            backgroundColor: '#1e2130',
            borderRadius: 8, borderLeft: '4px solid #81c784',
            fontSize: 13, color: '#ccc'
          }}>
            {result}
          </div>
        )}
      </div>

      {/* Full Pipeline */}
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 16, color: '#ffd54f', marginBottom: 4 }}>
          Full Pipeline → Seraph + Daedalus
        </h2>
        <p style={{ color: '#888', fontSize: 12, margin: '0 0 12px 0' }}>
          Seraph plans automatically, Daedalus executes each subtask
        </p>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            value={pipeline}
            onChange={e => setPipeline(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && runPipeline()}
            placeholder="Give RELAY a full task to coordinate end-to-end..."
            style={{
              flex: 1, padding: '10px 14px',
              backgroundColor: '#1e2130',
              border: '1px solid #333',
              borderRadius: 6, color: '#fff', fontSize: 14
            }}
          />
          <button
            onClick={runPipeline}
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: loading ? '#333' : '#ffd54f',
              color: loading ? '#888' : '#000',
              border: 'none', borderRadius: 6,
              fontWeight: 'bold', cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Running...' : 'Run Pipeline'}
          </button>
          <button
            onClick={() => { setPipeline(''); setPipelineResult(null) }}
            style={{
              padding: '10px 16px',
              backgroundColor: 'transparent',
              color: '#888',
              border: '1px solid #333',
              borderRadius: 6,
              cursor: 'pointer'
            }}
          >
            Clear
          </button>
        </div>
        {pipelineResult && (
          <div style={{
            marginTop: 16, padding: 16,
            backgroundColor: '#1e2130',
            borderRadius: 8, borderLeft: '4px solid #ffd54f',
          }}>
            <div style={{ color: '#ffd54f', fontWeight: 'bold', marginBottom: 12 }}>
              Pipeline Results — {pipelineResult.total_subtasks} subtasks executed
            </div>
            {pipelineResult.subtask_results?.map((item: any, i: number) => (
              <div key={i} style={{
                marginBottom: 12, padding: 12,
                backgroundColor: '#151822',
                borderRadius: 6
              }}>
                <div style={{ color: '#4fc3f7', fontSize: 12, marginBottom: 4 }}>
                  SUBTASK {i + 1}: {item.subtask}
                </div>
                <div style={{ color: '#81c784', fontSize: 13 }}>
                  {item.result}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Activity log */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <h2 style={{ fontSize: 16, color: '#888', margin: 0 }}>
            Agent Activity Log
          </h2>
          <button
            onClick={() => setLog([])}
            style={{
              padding: '4px 12px',
              backgroundColor: 'transparent',
              color: '#888',
              border: '1px solid #333',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: 12
            }}
          >
            Clear Log
          </button>
        </div>
        <div style={{
          backgroundColor: '#1e2130',
          borderRadius: 8, padding: 16,
          minHeight: 120, maxHeight: 300,
          overflowY: 'auto'
        }}>
          {log.length === 0 && (
            <div style={{ color: '#555', fontSize: 13 }}>
              No activity yet. Submit a task to get started.
            </div>
          )}
          {log.map((entry, i) => (
            <div key={i} style={{ fontSize: 13, marginBottom: 6, display: 'flex', gap: 12 }}>
              <span style={{ color: '#555', minWidth: 70 }}>{entry.time}</span>
              <span style={{
                color: agentColors[entry.agent] || '#fff',
                minWidth: 80, fontWeight: 'bold'
              }}>
                {entry.agent}
              </span>
              <span style={{
                color: entry.type === 'success' ? '#81c784' :
                       entry.type === 'error' ? '#e57373' : '#ccc'
              }}>
                {entry.message}
              </span>
            </div>
          ))}
        </div>
      </div>

    </main>
  )
}