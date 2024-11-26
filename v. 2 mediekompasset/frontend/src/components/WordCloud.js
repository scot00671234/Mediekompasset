import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';

const WordCloud = ({ mediaData }) => {
  const svgRef = useRef();
  
  useEffect(() => {
    if (!mediaData || !mediaData.length) return;
    
    // Saml alle ord og deres frekvenser
    const wordFrequencies = {};
    mediaData.forEach(item => {
      Object.entries(item.word_frequencies).forEach(([word, freq]) => {
        wordFrequencies[word] = (wordFrequencies[word] || 0) + freq;
      });
    });
    
    // Konverter til format der bruges af d3-cloud
    const words = Object.entries(wordFrequencies).map(([text, size]) => ({
      text,
      size: Math.sqrt(size) * 10 + 10 // Skaler størrelsen
    }));
    
    // Opsæt word cloud
    const width = 800;
    const height = 400;
    
    const layout = cloud()
      .size([width, height])
      .words(words)
      .padding(5)
      .rotate(() => (~~(Math.random() * 2) - 1) * 90)
      .fontSize(d => d.size)
      .on('end', draw);
      
    layout.start();
    
    function draw(words) {
      // Fjern eksisterende SVG
      d3.select(svgRef.current).selectAll('*').remove();
      
      // Opret ny word cloud
      const svg = d3.select(svgRef.current)
        .attr('width', width)
        .attr('height', height);
        
      const g = svg.append('g')
        .attr('transform', `translate(${width/2},${height/2})`);
        
      // Farve skala baseret på ord størrelse
      const color = d3.scaleLinear()
        .domain([0, d3.max(words, d => d.size)])
        .range(['#69b3a2', '#3498db']);
        
      g.selectAll('text')
        .data(words)
        .enter().append('text')
        .style('font-size', d => `${d.size}px`)
        .style('fill', d => color(d.size))
        .attr('text-anchor', 'middle')
        .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
        .text(d => d.text)
        .on('mouseover', function(event, d) {
          d3.select(this)
            .transition()
            .style('font-size', `${d.size * 1.2}px`)
            .style('fill', '#e74c3c');
        })
        .on('mouseout', function(event, d) {
          d3.select(this)
            .transition()
            .style('font-size', `${d.size}px`)
            .style('fill', color(d.size));
        });
    }
  }, [mediaData]);
  
  return (
    <div className="word-cloud-container">
      <h2>Ordsky over mest brugte ord</h2>
      <div className="word-cloud">
        <svg ref={svgRef}></svg>
      </div>
      <div className="word-cloud-info">
        <p>
          Denne visualisering viser de mest brugte ord på tværs af alle analyserede artikler.
          Størrelsen af ordet indikerer hvor ofte det bliver brugt, og farven indikerer ordets
          relative frekvens.
        </p>
        <ul>
          <li>Hover over et ord for at fremhæve det</li>
          <li>Blå nuancer indikerer højere frekvens</li>
          <li>Grønne nuancer indikerer lavere frekvens</li>
        </ul>
      </div>
    </div>
  );
};

export default WordCloud;
