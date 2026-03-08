/**
 * 데이터 분석 유틸리티
 */

// 1. 이동평균 (Moving Average) 계산
export const calculateMA = (data, windowSize, key) => {
    return data.map((val, index, arr) => {
        if (index < windowSize - 1) return null;
        const window = arr.slice(index - windowSize + 1, index + 1);
        const sum = window.reduce((acc, curr) => acc + curr[key], 0);
        return sum / windowSize;
    });
};

// 2. 요일별 평균 분석
export const groupByDayOfWeek = (data) => {
    const days = ['일', '월', '화', '수', '목', '금', '토'];
    const stats = days.map(day => ({ day, Gemini: [], Claude: [] }));

    data.forEach(d => {
        const dayIndex = new Date(d.Date).getDay();
        stats[dayIndex].Gemini.push(d.Gemini_Ratio);
        stats[dayIndex].Claude.push(d.Claude_Ratio);
    });

    return stats.map(s => ({
        day: s.day,
        Gemini: s.Gemini.length ? (s.Gemini.reduce((a, b) => a + b, 0) / s.Gemini.length).toFixed(2) : 0,
        Claude: s.Claude.length ? (s.Claude.reduce((a, b) => a + b, 0) / s.Claude.length).toFixed(2) : 0,
    }));
};

// 3. 월별/분기별 합계/평균 분석
export const groupByPeriod = (data, periodType = 'month') => {
    const groups = {};

    data.forEach(d => {
        const date = new Date(d.Date);
        let key;
        if (periodType === 'month') {
            key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        } else {
            key = `${date.getFullYear()}-Q${Math.floor(date.getMonth() / 3) + 1}`;
        }

        if (!groups[key]) {
            groups[key] = { label: key, Gemini: [], Claude: [] };
        }
        groups[key].Gemini.push(d.Gemini_Ratio);
        groups[key].Claude.push(d.Claude_Ratio);
    });

    return Object.values(groups).map(g => ({
        label: g.label,
        Gemini: (g.Gemini.reduce((a, b) => a + b, 0) / g.Gemini.length).toFixed(2),
        Claude: (g.Claude.reduce((a, b) => a + b, 0) / g.Claude.length).toFixed(2),
    }));
};

// 4. 상관계수 (Pearson Correlation Coefficient) 계산
export const calculateCorrelation = (x, y) => {
    const n = x.length;
    if (n !== y.length || n === 0) return 0;

    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((acc, val, i) => acc + val * y[i], 0);
    const sumX2 = x.reduce((acc, val) => acc + val * val, 0);
    const sumY2 = y.reduce((acc, val) => acc + val * val, 0);

    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

    if (denominator === 0) return 0;
    return (numerator / denominator).toFixed(4);
};
