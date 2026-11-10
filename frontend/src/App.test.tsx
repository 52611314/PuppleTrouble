import { afterEach, expect, test, vi } from 'vitest'
import { render, screen, cleanup } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'

afterEach(() => { cleanup(); vi.unstubAllGlobals() })

test('服务不可用时结束加载并显示可恢复的提示', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('network unavailable')))
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
    render(<QueryClientProvider client={client}><App /></QueryClientProvider>)
    expect(await screen.findByRole('heading', { name: '后端尚未连接' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '重新检查连接' })).toBeEnabled()
})
