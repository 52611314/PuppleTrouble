import { useQuery } from '@tanstack/react-query'
import { API_BASE_URL, fetchHealth } from './shared/api/client'

const colors = ['#7550A5', '#C4ADD9', '#F0C1A4', '#F0E9DF', '#394E4B']

export default function App() {
    const health = useQuery({ queryKey: ['health'], queryFn: fetchHealth, retry: false })
    return <main className="shell">
        <header className="topbar"><a href="/" className="brand"><span className="brand-mark">P</span>玩犊紫<span className="brand-en">PuppleTrouble</span></a><span className="tag">起步，从一种颜色开始</span></header>
        <section className="hero">
            <div><p className="eyebrow">COLOR IS A LANGUAGE</p><h1>让喜欢的颜色，<br />成为你的表达。</h1><p className="intro">从一抹紫色出发，探索作品里的配色关系。<br />颜色探索、实例讲解与配色工作台将在后续开发中加入。</p></div>
            <div className="color-study" aria-label="本地示例配色"><div className="study-label">A STUDY IN PURPLE <span>01 / 05</span></div><div className="color-shapes"><i /><i /><i /></div><div className="swatches">{colors.map(color => <div key={color}><span style={{ background: color }} /><code>{color}</code></div>)}</div><small>本地示例配色 · 用于工程首页展示</small></div>
        </section>
        <section className="connection" aria-label="服务连接状态">
            <div><p className="eyebrow">CONNECTION</p><h2>{health.isPending ? '正在检查后端连接…' : health.isError ? '后端尚未连接' : '后端连接正常'}</h2><p role="status">{health.isError ? '请按启动文档启动后端，然后重新检查连接。' : health.data ? `${health.data.data.service} · v${health.data.data.version} · 工程初始化版本` : '连接本地服务，确认开发环境已准备好。'}</p><code className="api-address">{API_BASE_URL}</code></div>
            <div className="actions"><button disabled={health.isFetching} onClick={() => void health.refetch()}>{health.isFetching ? '检查中…' : '重新检查连接'}</button><a href={API_BASE_URL.replace(/\/api\/v1$/, '/docs')} target="_blank" rel="noreferrer">查看接口文档 ↗</a></div>
        </section>
        <footer>玩犊紫 · PuppleTrouble <span>工程骨架已建立，产品功能持续开发中。</span></footer>
    </main>
}
