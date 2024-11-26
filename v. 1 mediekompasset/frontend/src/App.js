import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import BiasChart from './components/BiasChart';
import MediaComparison from './components/MediaComparison';
import WordCloud from './components/WordCloud';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  const [mediaData, setMediaData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMediaData();
  }, []);

  const fetchMediaData = async () => {
    try {
      const response = await fetch('http://localhost:8000/analyze/all');
      const data = await response.json();
      setMediaData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Navigation />
        <Switch>
          <Route exact path="/">
            <Dashboard mediaData={mediaData} />
          </Route>
          <Route path="/bias-chart">
            <BiasChart mediaData={mediaData} />
          </Route>
          <Route path="/comparison">
            <MediaComparison mediaData={mediaData} />
          </Route>
          <Route path="/word-cloud">
            <WordCloud mediaData={mediaData} />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
