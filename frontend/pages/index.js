import { useEffect, useState } from 'react';

export default function Dashboard() {
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/data/daily_predictions.json')
            .then((res) => res.json())
            .then((data) => {
                setPredictions(data);
                setLoading(false);
            })
            .catch((err) => console.error("Error fetching data:", err));
    }, []);

    if (loading) return <div style={{ padding: '2rem' }}>Loading the edge...</div>;

    return (
        <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
            <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Daily Quant Predictions</h1>
            <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
                {predictions.map((match, index) => (
                    <div key={index} style={{
                        border: '1px solid #ccc',
                        padding: '1.5rem',
                        borderRadius: '8px',
                        backgroundColor: match.modelValueEdge ? '#e6ffe6' : '#f9f9f9'
                    }}>
                        <h2 style={{ margin: '0 0 1rem 0' }}>{match.homeTeam} vs {match.awayTeam}</h2>
                        <p><strong>Home Win:</strong> {match.homeWinProb}%</p>
                        <p><strong>Draw:</strong> {match.drawProb}%</p>
                        <p><strong>Away Win:</strong> {match.awayWinProb}%</p>
                        <hr style={{ margin: '1rem 0' }} />
                        <p>
                            <strong>Action:</strong> {match.recommendedBet} 
                            {match.modelValueEdge && ' 🟢 (Value Found)'}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
