import { z } from 'zod'

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1').replace(/\/$/, '')

const healthSchema = z.object({
    data: z.object({ status: z.literal('ok'), service: z.string(), version: z.string(), stage: z.string() }),
    request_id: z.string(),
})

export async function fetchHealth() {
    const response = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(5000) })
    if (!response.ok) throw new Error('服务暂时无法连接')
    return healthSchema.parse(await response.json())
}
