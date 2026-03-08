import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

export const useTrendData = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // fetch는 로컬 파일(public 폴더나 서버 루트)을 대상으로 하므로
                // Vite 개발 서버에서 data/ 폴더를 접근 가능하게 해야 함. 
                // 여기서는 데이터 수집 경로가 /data/ai_trend_data.csv 임을 가정.
                const response = await fetch('/data/ai_trend_data.csv');
                const reader = response.body.getReader();
                const result = await reader.read();
                const decoder = new TextDecoder('utf-8');
                const csv = decoder.decode(result.value);

                Papa.parse(csv, {
                    header: true,
                    dynamicTyping: true,
                    complete: (results) => {
                        setData(results.data.filter(row => row.Date)); // 빈 행 제거
                        setLoading(false);
                    },
                    error: (err) => {
                        setError(err.message);
                        setLoading(false);
                    }
                });
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return { data, loading, error };
};
