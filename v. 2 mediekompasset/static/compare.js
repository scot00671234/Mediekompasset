// Media comparison functionality
let selectedMedia = new Set();

function updateComparison() {
    const checkboxes = document.querySelectorAll('.media-checkbox');
    selectedMedia.clear();
    
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedMedia.add(checkbox.value);
        }
    });

    const comparisonResults = document.getElementById('comparison-results');
    if (selectedMedia.size >= 2) {
        comparisonResults.classList.remove('comparison-hidden');
        updateBiasComparison();
        updateMetricsComparison();
        updateTopicsComparison();
    } else {
        comparisonResults.classList.add('comparison-hidden');
    }
}

function updateBiasComparison() {
    const biasIndicators = document.getElementById('bias-indicators');
    biasIndicators.innerHTML = '';

    selectedMedia.forEach(mediaId => {
        const media = mediaData[mediaId];
        const position = (media.bias + 1) * 50; // Convert -1...1 to 0...100

        const indicator = document.createElement('div');
        indicator.className = 'bias-comparison-indicator';
        indicator.style.left = `${position}%`;
        indicator.style.backgroundColor = getMediaColor(mediaId);
        
        const label = document.createElement('div');
        label.className = 'bias-comparison-label';
        label.textContent = media.name;
        label.style.color = getMediaColor(mediaId);
        
        indicator.appendChild(label);
        biasIndicators.appendChild(indicator);
    });
}

function updateMetricsComparison() {
    updateMetricBars('factuality-comparison', 'factuality');
    updateMetricBars('diversity-comparison', 'source_diversity');
    updateMetricBars('balance-comparison', 'topic_balance');
}

function updateMetricBars(elementId, metricKey) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';

    selectedMedia.forEach(mediaId => {
        const media = mediaData[mediaId];
        const value = media.metrics[metricKey] * 100;

        const barContainer = document.createElement('div');
        barContainer.className = 'metric-bar-container';

        const label = document.createElement('div');
        label.className = 'metric-bar-label';
        label.textContent = media.name;
        label.style.color = getMediaColor(mediaId);

        const barWrapper = document.createElement('div');
        barWrapper.className = 'metric-bar-wrapper';

        const bar = document.createElement('div');
        bar.className = 'metric-bar';
        bar.style.width = `${value}%`;
        bar.style.backgroundColor = getMediaColor(mediaId);

        const valueLabel = document.createElement('span');
        valueLabel.className = 'metric-value';
        valueLabel.textContent = `${Math.round(value)}%`;

        barWrapper.appendChild(bar);
        barWrapper.appendChild(valueLabel);
        barContainer.appendChild(label);
        barContainer.appendChild(barWrapper);
        container.appendChild(barContainer);
    });
}

function updateTopicsComparison() {
    const container = document.getElementById('topics-comparison');
    container.innerHTML = '';

    selectedMedia.forEach(mediaId => {
        const media = mediaData[mediaId];
        const row = document.createElement('div');
        row.className = 'topics-row mb-3';
        
        const label = document.createElement('div');
        label.className = 'topics-label';
        label.textContent = media.name;
        label.style.color = getMediaColor(mediaId);
        
        const topics = document.createElement('div');
        topics.className = 'topics-list';
        
        media.top_topics.forEach(topic => {
            const topicTag = document.createElement('span');
            topicTag.className = 'topic-tag';
            topicTag.textContent = topic;
            topicTag.style.borderColor = getMediaColor(mediaId);
            topicTag.style.color = getMediaColor(mediaId);
            topics.appendChild(topicTag);
        });
        
        row.appendChild(label);
        row.appendChild(topics);
        container.appendChild(row);
    });
}

function getMediaColor(mediaId) {
    const colors = {
        'dr': '#C70000',         // DR Red
        'tv2': '#E4002B',        // TV2 Red
        'politiken': '#333333',  // Dark Gray
        'berlingske': '#00447C', // Dark Blue
        'information': '#D14124', // Orange Red
        'jyllandsposten': '#005293', // Blue
        'ekstrabladet': '#FF5722', // Deep Orange
        'bt': '#E65100',         // Dark Orange
        'kristeligt-dagblad': '#1B5E20', // Dark Green
        'borsen': '#F9A825',     // Dark Yellow
        'altinget': '#4A148C',   // Deep Purple
        'finans': '#0277BD'      // Light Blue
    };
    return colors[mediaId] || '#666666';
}
