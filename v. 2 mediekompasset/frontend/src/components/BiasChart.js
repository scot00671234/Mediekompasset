import React from 'react';
import { Bar } from 'react-chartjs-2';

const BiasChart = ({ mediaData }) => {
  const chartData = {
    labels: mediaData.map(item => item.source),
    datasets: [
      {
        label: 'Politisk Bias Score',
        data: mediaData.map(item => item.bias_score),
        backgroundColor: mediaData.map(item => {
          const score = item.bias_score;
          if (score < -0.33) return 'rgba(255, 99, 132, 0.6)';  // Rød (venstre)
          if (score > 0.33) return 'rgba(54, 162, 235, 0.6)';   // Blå (højre)
          return 'rgba(255, 206, 86, 0.6)';                     // Gul (centrum)
        }),
        borderWidth: 1
      }
    ]
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Bias Score (-1 = Venstre, 1 = Højre)'
        }
      }
    },
    plugins: {
      title: {
        display: true,
        text: 'Politisk Bias på tværs af danske medier'
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const score = context.raw;
            let bias = 'Neutral';
            if (score < -0.33) bias = 'Venstreorienteret';
            if (score > 0.33) bias = 'Højreorienteret';
            return `Bias Score: ${score.toFixed(2)} (${bias})`;
          }
        }
      }
    }
  };

  return (
    <div className="bias-chart">
      <Bar data={chartData} options={options} />
      <div className="chart-legend">
        <div className="legend-item">
          <span className="color-box left"></span>
          <span>Venstreorienteret</span>
        </div>
        <div className="legend-item">
          <span className="color-box center"></span>
          <span>Centrum</span>
        </div>
        <div className="legend-item">
          <span className="color-box right"></span>
          <span>Højreorienteret</span>
        </div>
      </div>
    </div>
  );
};

export default BiasChart;
