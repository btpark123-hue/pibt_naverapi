import React, { useMemo, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    RadialLinearScale,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Line, Bar, Radar } from 'react-chartjs-2';
import { useTrendData } from './utils/csvLoader';
import * as analysis from './utils/analytics';
import {
    TrendingUp, Activity, Database, Cpu,
    Calendar, PieChart, BarChart3, Info,
    ArrowUpRight, ArrowDownRight, Minus
} from 'lucide-react';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    RadialLinearScale,
    Title,
    Tooltip,
    Legend,
    Filler
);

function App() {
    const { data, loading, error } = useTrendData();
    const [activeTab, setActiveTab] = useState('overview'); // overview, periodic, correlation, table

    const analytics = useMemo(() => {
        if (!data.length) return null;

        const geminiValues = data.map(d => d.Gemini_Ratio);
        const claudeValues = data.map(d => d.Claude_Ratio);

        const ma7G = analysis.calculateMA(data, 7, 'Gemini_Ratio');
        const ma7C = analysis.calculateMA(data, 7, 'Claude_Ratio');

        const dayStats = analysis.groupByDayOfWeek(data);
        const monthStats = analysis.groupByPeriod(data, 'month');
        const quarterStats = analysis.groupByPeriod(data, 'quarter');
        const correlation = analysis.calculateCorrelation(geminiValues, claudeValues);

        const avg = values => (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);
        const max = values => Math.max(...values).toFixed(1);

        // 트렌드 방향성 계산
        const getTrend = (values) => {
            const last = values[values.length - 1];
            const prev = values[values.length - 8] || values[0]; // 1주일 전과 비교
            const diff = last - prev;
            return { diff: diff.toFixed(1), direction: diff > 0 ? 'up' : diff < 0 ? 'down' : 'stable' };
        };

        return {
            ma7: { Gemini: ma7G, Claude: ma7C },
            dayStats,
            monthStats,
            quarterStats,
            correlation,
            summary: {
                gemini: { avg: avg(geminiValues), max: max(geminiValues), trend: getTrend(geminiValues) },
                claude: { avg: avg(claudeValues), max: max(claudeValues), trend: getTrend(claudeValues) }
            }
        };
    }, [data]);

    const chartConfigs = useMemo(() => {
        if (!data.length || !analytics) return null;

        // 1. 메인 트렌드 (With 7-day MA)
        const mainChart = {
            labels: data.map(d => d.Date),
            datasets: [
                {
                    label: 'Gemini (Daily)',
                    data: data.map(d => d.Gemini_Ratio),
                    borderColor: 'rgba(99, 102, 241, 0.3)',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.4,
                },
                {
                    label: 'Gemini (7d MA)',
                    data: analytics.ma7.Gemini,
                    borderColor: '#6366f1',
                    borderWidth: 3,
                    pointRadius: 0,
                    tension: 0.4,
                    fill: false,
                },
                {
                    label: 'Claude (Daily)',
                    data: data.map(d => d.Claude_Ratio),
                    borderColor: 'rgba(236, 72, 153, 0.3)',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.4,
                },
                {
                    label: 'Claude (7d MA)',
                    data: analytics.ma7.Claude,
                    borderColor: '#ec4899',
                    borderWidth: 3,
                    pointRadius: 0,
                    tension: 0.4,
                    fill: false,
                }
            ]
        };

        // 2. 월별 비교
        const monthChart = {
            labels: analytics.monthStats.map(s => s.label),
            datasets: [
                { label: 'Gemini', data: analytics.monthStats.map(s => s.Gemini), backgroundColor: '#6366f1' },
                { label: 'Claude', data: analytics.monthStats.map(s => s.Claude), backgroundColor: '#ec4899' }
            ]
        };

        // 3. 요일별 분석 (Radar)
        const dayChart = {
            labels: analytics.dayStats.map(s => s.day),
            datasets: [
                {
                    label: 'Gemini',
                    data: analytics.dayStats.map(s => s.Gemini),
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
                    borderColor: '#6366f1',
                    pointBackgroundColor: '#6366f1',
                },
                {
                    label: 'Claude',
                    data: analytics.dayStats.map(s => s.Claude),
                    backgroundColor: 'rgba(236, 72, 153, 0.2)',
                    borderColor: '#ec4899',
                    pointBackgroundColor: '#ec4899',
                }
            ]
        };

        return { mainChart, monthChart, dayChart };
    }, [data, analytics]);

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#94a3b8', font: { family: 'Pretendard' } } }
        },
        scales: {
            x: { ticks: { color: '#64748b' }, grid: { display: false } },
            y: { ticks: { color: '#64748b' }, grid: { color: 'rgba(255,255,255,0.05)' } }
        }
    };

    if (loading) return <div className="loading-screen">Deep Analytics Engine Loading...</div>;
    if (error) return <div className="error-screen">Error: {error}</div>;

    return (
        <div className="container">
            <header className="header">
                <h1 className="title">AI Deep Insights</h1>
                <p className="subtitle">Gemini vs Claude 다차원 검색 트렌드 분석 리포트</p>
            </header>

            <div className="glass-card main-dashboard">
                <nav className="tab-control scrollable">
                    <button className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}><Activity size={18} /> 트렌드 개요</button>
                    <button className={`tab-btn ${activeTab === 'periodic' ? 'active' : ''}`} onClick={() => setActiveTab('periodic')}><BarChart3 size={18} /> 기간/요일 분석</button>
                    <button className={`tab-btn ${activeTab === 'correlation' ? 'active' : ''}`} onClick={() => setActiveTab('correlation')}><PieChart size={18} /> 상관성/인사이트</button>
                    <button className={`tab-btn ${activeTab === 'table' ? 'active' : ''}`} onClick={() => setActiveTab('table')}><Database size={18} /> 원본 데이터</button>
                </nav>

                <div className="content-area">
                    {activeTab === 'overview' && (
                        <div className="fade-in">
                            <div className="chart-container large">
                                <Line data={chartConfigs.mainChart} options={{ ...commonOptions, plugins: { ...commonOptions.plugins, title: { display: true, text: '일별 추이 및 7일 이동평균선', color: '#f8fafc' } } }} />
                            </div>
                            <div className="stats-grid">
                                <StatCard title="Gemini 1년 평균" value={analytics.summary.gemini.avg} trend={analytics.summary.gemini.trend} color="#6366f1" />
                                <StatCard title="Claude 1년 평균" value={analytics.summary.claude.avg} trend={analytics.summary.claude.trend} color="#ec4899" />
                                <StatCard title="검색 상관계수" value={analytics.correlation} info="1에 가까울수록 동반 상승/하락" />
                            </div>
                        </div>
                    )}

                    {activeTab === 'periodic' && (
                        <div className="fade-in grid-2">
                            <div className="chart-container">
                                <Bar data={chartConfigs.monthChart} options={{ ...commonOptions, plugins: { title: { display: true, text: '월별 평균 검색 비중', color: '#f8fafc' } } }} />
                            </div>
                            <div className="chart-container">
                                <Radar data={chartConfigs.dayChart} options={{ ...commonOptions, scales: { r: { grid: { color: 'rgba(255,255,255,0.1)' }, pointLabels: { color: '#94a3b8' } } } }} />
                            </div>
                        </div>
                    )}

                    {activeTab === 'correlation' && (
                        <div className="fade-in report-view">
                            <div className="glass-card inner">
                                <h3>📜 데이터 종합 분석 결론</h3>
                                <div className="report-content">
                                    <p>1. <strong>성장 모멘텀</strong>: Gemini의 평균 지수는 {analytics.summary.gemini.avg}로 Claude({analytics.summary.claude.avg}) 대비 우위에 있습니다.</p>
                                    <p>2. <strong>상관성</strong>: 두 모델의 상관계수는 {analytics.correlation}입니다. {analytics.correlation > 0.7 ? '매우 높은 양의 상관관계가 관찰되며, AI 시장 전체의 관심도가 함께 움직이고 있음' : '독자적인 트렌드 흐름을 보이고 있음'}을 시사합니다.</p>
                                    <p>3. <strong>요일별 패턴</strong>: 데이터 분석 결과, {analytics.dayStats.sort((a, b) => b.Gemini - a.Gemini)[0].day}요일에 가장 높은 검색 활성도가 나타났습니다.</p>
                                    <p>4. <strong>변동성</strong>: Peak 수치는 Gemini {analytics.summary.gemini.max}, Claude {analytics.summary.claude.max}로 시장 점유율 확대를 위한 격전이 지속되고 있습니다.</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'table' && (
                        <div className="fade-in table-view">
                            <div className="table-wrapper">
                                <table className="data-table">
                                    <thead><tr><th>날짜</th><th>Gemini</th><th>Claude</th></tr></thead>
                                    <tbody>
                                        {[...data].reverse().slice(0, 30).map((row, idx) => (
                                            <tr key={idx}>
                                                <td>{row.Date}</td>
                                                <td className="cell-gemini">{row.Gemini_Ratio.toFixed(2)}</td>
                                                <td className="cell-claude">{row.Claude_Ratio.toFixed(2)}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                                <p className="table-info">* 최근 30일 데이터만 표시됩니다. 전체 데이터는 CSV를 참조하세요.</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, trend, info, color }) {
    return (
        <div className="stat-item">
            <div className="stat-label">{title}</div>
            <div className="stat-value" style={{ color }}>{value}</div>
            {trend && (
                <div className={`trend-tag ${trend.direction}`}>
                    {trend.direction === 'up' ? <ArrowUpRight size={14} /> : trend.direction === 'down' ? <ArrowDownRight size={14} /> : <Minus size={14} />}
                    {trend.diff}%
                </div>
            )}
            {info && <div className="stat-info">{info}</div>}
        </div>
    );
}

export default App;
