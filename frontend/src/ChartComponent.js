
import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';

const ChartComponent = () => {
    const chartContainerRef = useRef();
    const chartRef = useRef();
    const candleSeriesRef = useRef();
    const [llmSignals, setLlmSignals] = useState([]);

    useEffect(() => {
        // Initialize chart
        chartRef.current = createChart(chartContainerRef.current, {
            width: chartContainerRef.current.clientWidth,
            height: 600,
            layout: {
                backgroundColor: '#0e1726',
                textColor: '#d1d4dc',
            },
            grid: {
                vertLines: {
                    color: 'rgba(42, 46, 57, 0.5)',
                },
                horzLines: {
                    color: 'rgba(42, 46, 57, 0.5)',
                },
            },
            timeScale: {
                timeVisible: true,
                secondsVisible: false,
            }
        });

        candleSeriesRef.current = chartRef.current.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderDownColor: '#ef5350',
            borderUpColor: '#26a69a',
            wickDownColor: '#ef5350',
            wickUpColor: '#26a69a',
        });

        // Fetch historical data
        fetch('http://localhost:8000/api/history')
            .then(res => res.json())
            .then(data => {
                const formattedData = data.map(d => ({
                    time: new Date(d.time).getTime() / 1000,
                    open: d.open,
                    high: d.high,
                    low: d.low,
                    close: d.close,
                }));
                candleSeriesRef.current.setData(formattedData);
            });

        // Setup WebSocket
        const ws = new WebSocket('ws://localhost:8000/ws');

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'kline') {
                const candle = {
                    time: new Date(message.data.time).getTime() / 1000,
                    open: message.data.open,
                    high: message.data.high,
                    low: message.data.low,
                    close: message.data.close,
                };
                candleSeriesRef.current.update(candle);
            } else if (message.type === 'llm_analysis') {
                const analysis = message.data;
                const signalTime = new Date(analysis.timestamp).getTime() / 1000;
                
                let newSignal = {
                    time: signalTime,
                    position: analysis.signal === 'bullish' ? 'aboveBar' : 'belowBar',
                    color: analysis.signal === 'bullish' ? '#26a69a' : '#ef5350',
                    shape: analysis.signal === 'bullish' ? 'arrowUp' : 'arrowDown',
                    text: `${analysis.signal.toUpperCase()} @ ${analysis.target_price.toFixed(2)}`
                };
                if(analysis.signal === 'neutral') {
                    newSignal.shape = 'circle';
                    newSignal.color = '#d1d4dc';
                    newSignal.position = 'aboveBar';
                }

                setLlmSignals(prevSignals => [...prevSignals, newSignal]);
            }
        };

        // Cleanup on component unmount
        return () => {
            ws.close();
            chartRef.current.remove();
        };
    }, []);

    useEffect(() => {
        if (candleSeriesRef.current) {
            candleSeriesRef.current.setMarkers(llmSignals);
        }
    }, [llmSignals]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundColor: '#0e1726', color: 'white' }}>
            <h1>LLM K-Line Analysis</h1>
            <div ref={chartContainerRef} style={{ width: '90%', position: 'relative' }} />
            <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#1c273a', borderRadius: '5px', width: '90%' }}>
                <h2>Latest LLM Signal:</h2>
                {llmSignals.length > 0 ? (
                    <p>{llmSignals[llmSignals.length - 1].text}</p>
                ) : (
                    <p>Waiting for analysis...</p>
                )}
            </div>
        </div>
    );
};

export default ChartComponent;
