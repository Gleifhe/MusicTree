/**
 * MusicTree — Full D3 Force-Directed Graph (Homepage)
 * Uses global GRAPH_DATA injected by Hugo template.
 */
(function () {
  const NODE_COLORS = {
    artist: '#4e79a7',
    person: '#59a14f',
    album:  '#b07aa1',
    song:   '#f28e2b',
  };

  const NODE_RADIUS = {
    artist: 18,
    person: 13,
    album:  15,
    song:   10,
  };

  const RELATION_LABELS = {
    'member-of':    'member',
    'released':     'released',
    'appears-on':   'on',
    'performed-by': 'performed',
    'produced-by':  'produced',
    'written-by':   'wrote',
    'played':       'played',
  };

  const container = document.getElementById('graph-container');
  const svg = d3.select('#graph-svg');
  const tooltip = document.getElementById('graph-tooltip');

  const width  = container.clientWidth;
  const height = container.clientHeight;

  // Clone data so simulation can mutate it
  const rawData = window.GRAPH_DATA || { nodes: [], links: [] };
  const allNodes = rawData.nodes.map(d => ({ ...d }));
  const allLinks = rawData.links.map(d => ({ ...d }));

  let activeTypes = new Set(['artist', 'person', 'album', 'song']);
  let searchTerm = '';

  // ── SVG setup ───────────────────────────────────────────────────────────
  svg.attr('width', width).attr('height', height);

  const defs = svg.append('defs');

  // Arrow marker per type
  Object.entries(NODE_COLORS).forEach(([type, color]) => {
    defs.append('marker')
      .attr('id', `arrow-${type}`)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 20)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', color)
        .attr('opacity', 0.6);
  });

  const gRoot = svg.append('g').attr('class', 'graph-root');

  const zoom = d3.zoom()
    .scaleExtent([0.15, 4])
    .on('zoom', e => {
      gRoot.attr('transform', e.transform);
      updateClusterOpacity(e.transform.k);
    });

  svg.call(zoom);

  document.getElementById('btn-reset').addEventListener('click', () => {
    svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
  });

  // ── Cluster label opacity based on zoom scale ──────────────────────────────
  // Artist labels: fade in 0.65→0.45, fade out at higher zoom
  // Scene labels:  fade in 0.40→0.25 (only visible very zoomed out)
  function updateClusterOpacity(scale) {
    const artistOpacity = Math.max(0, Math.min(0.55, (0.65 - scale) / 0.2 * 0.55));
    const sceneOpacity  = Math.max(0, Math.min(0.12, (0.38 - scale) / 0.15 * 0.12));
    gRoot.selectAll('.cluster-artist-labels text').attr('opacity', artistOpacity);
    gRoot.selectAll('.cluster-scene-labels text').attr('opacity', sceneOpacity);
  }

  // ── Simulation ──────────────────────────────────────────────────────────
  let simulation, gLink, gNode, linkEls, nodeEls;

  function buildGraph() {
    // Filter nodes by active types and search
    const visibleNodes = allNodes.filter(n => {
      if (!activeTypes.has(n.type)) return false;
      if (searchTerm) return n.label.toLowerCase().includes(searchTerm);
      return true;
    });

    const visibleIds = new Set(visibleNodes.map(n => n.id));

    const visibleLinks = allLinks.filter(l => {
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      return visibleIds.has(srcId) && visibleIds.has(tgtId);
    });

    // Reset to string IDs for re-simulation
    const nodeData = visibleNodes.map(d => ({ ...d }));
    const linkData = visibleLinks.map(d => ({
      source: typeof d.source === 'object' ? d.source.id : d.source,
      target: typeof d.target === 'object' ? d.target.id : d.target,
      relation: d.relation,
    }));

    if (simulation) simulation.stop();

    gRoot.selectAll('*').remove();

    // ── Cluster labels (behind everything, visible when zoomed out) ──────────
    // Artist-level: one label per artist node
    const artistNodes = nodeData.filter(n => n.type === 'artist');
    const gArtistLabels = gRoot.append('g').attr('class', 'cluster-artist-labels');
    gArtistLabels.selectAll('text')
      .data(artistNodes, d => d.id)
      .join('text')
        .attr('text-anchor', 'middle')
        .attr('font-size', 56)
        .attr('font-weight', 900)
        .attr('fill', NODE_COLORS.artist)
        .attr('opacity', 0)
        .attr('pointer-events', 'none')
        .style('letter-spacing', '1px')
        .text(d => d.label);

    // Scene-level: one label per unique scene (centroid of all artist nodes in scene)
    const sceneMap = {};
    artistNodes.forEach(n => {
      if (n.scene) (sceneMap[n.scene] = sceneMap[n.scene] || []).push(n);
    });
    const sceneData = Object.entries(sceneMap)
      .filter(([, nodes]) => nodes.length >= 2)
      .map(([scene, nodes]) => ({ scene, nodes }));

    const gSceneLabels = gRoot.append('g').attr('class', 'cluster-scene-labels');
    gSceneLabels.selectAll('text')
      .data(sceneData, d => d.scene)
      .join('text')
        .attr('text-anchor', 'middle')
        .attr('font-size', 110)
        .attr('font-weight', 900)
        .attr('fill', '#ffffff')
        .attr('opacity', 0)
        .attr('pointer-events', 'none')
        .style('letter-spacing', '3px')
        .text(d => d.scene);

    // Links
    gLink = gRoot.append('g').attr('class', 'links');
    linkEls = gLink.selectAll('line')
      .data(linkData)
      .join('line')
        .attr('class', 'graph-link')
        .attr('marker-end', d => {
          const tgtNode = nodeData.find(n => n.id === d.target);
          return tgtNode ? `url(#arrow-${tgtNode.type})` : '';
        });

    // Link labels
    const linkLabels = gRoot.append('g').attr('class', 'link-labels')
      .selectAll('text')
      .data(linkData)
      .join('text')
        .attr('class', 'link-label')
        .text(d => RELATION_LABELS[d.relation] || d.relation || '');

    // Nodes
    gNode = gRoot.append('g').attr('class', 'nodes');
    nodeEls = gNode.selectAll('g.graph-node')
      .data(nodeData, d => d.id)
      .join('g')
        .attr('class', 'graph-node')
        .call(d3.drag()
          .on('start', dragStart)
          .on('drag',  dragged)
          .on('end',   dragEnd))
        .on('click', (event, d) => {
          if (d.url) window.location.href = d.url;
        })
        .on('mouseover', (event, d) => showTooltip(event, d))
        .on('mousemove', (event, d) => moveTooltip(event))
        .on('mouseout', hideTooltip);

    nodeEls.append('circle')
      .attr('r', d => NODE_RADIUS[d.type] || 12)
      .attr('fill', d => NODE_COLORS[d.type] || '#888')
      .attr('stroke', d => d3.color(NODE_COLORS[d.type] || '#888').brighter(0.6));

    nodeEls.append('text')
      .attr('dy', d => -(NODE_RADIUS[d.type] || 12) - 4)
      .attr('text-anchor', 'middle')
      .text(d => d.label.length > 20 ? d.label.slice(0, 18) + '…' : d.label);

    simulation = d3.forceSimulation(nodeData)
      .force('link', d3.forceLink(linkData).id(d => d.id).distance(d => {
        // Longer distance for song–album links to reduce clutter
        return d.relation === 'appears-on' ? 70 : 110;
      }))
      .force('charge', d3.forceManyBody().strength(-220))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(d => (NODE_RADIUS[d.type] || 12) + 18))
      .on('tick', () => {
        linkEls
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);

        linkLabels
          .attr('x', d => (d.source.x + d.target.x) / 2)
          .attr('y', d => (d.source.y + d.target.y) / 2);

        nodeEls.attr('transform', d => `translate(${d.x},${d.y})`);

        // Move artist cluster labels to artist node positions
        const posById = {};
        nodeData.forEach(n => { posById[n.id] = n; });
        gArtistLabels.selectAll('text')
          .attr('x', d => { const n = posById[d.id]; return n ? n.x : 0; })
          .attr('y', d => { const n = posById[d.id]; return n ? n.y + 24 : 0; });

        // Move scene labels to centroid of each scene's artist nodes
        gSceneLabels.selectAll('text')
          .attr('x', d => {
            const xs = d.nodes.map(n => (posById[n.id] || n).x);
            return xs.reduce((a, b) => a + b, 0) / xs.length;
          })
          .attr('y', d => {
            const ys = d.nodes.map(n => (posById[n.id] || n).y);
            return ys.reduce((a, b) => a + b, 0) / ys.length;
          });
      });
  }

  // ── Drag ────────────────────────────────────────────────────────────────
  function dragStart(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x; d.fy = d.y;
  }
  function dragged(event, d) { d.fx = event.x; d.fy = event.y; }
  function dragEnd(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null; d.fy = null;
  }

  // ── Tooltip ─────────────────────────────────────────────────────────────
  function showTooltip(event, d) {
    tooltip.classList.remove('hidden');
    tooltip.innerHTML = `
      <div class="tooltip-type">${d.type}</div>
      <div class="tooltip-title">${d.label}</div>
      ${d.meta ? `<div style="font-size:0.78rem;color:#8888aa;margin-top:0.2rem">${d.meta}</div>` : ''}
      ${d.url ? `<div style="font-size:0.75rem;color:#7c6af5;margin-top:0.3rem">Click to view ↗</div>` : ''}
    `;
    moveTooltip(event);
  }
  function moveTooltip(event) {
    const rect = container.getBoundingClientRect();
    let x = event.clientX - rect.left + 14;
    let y = event.clientY - rect.top + 14;
    if (x + 200 > rect.width)  x = event.clientX - rect.left - 214;
    if (y + 80  > rect.height) y = event.clientY - rect.top  - 80;
    tooltip.style.left = x + 'px';
    tooltip.style.top  = y + 'px';
  }
  function hideTooltip() { tooltip.classList.add('hidden'); }

  // ── Filters ─────────────────────────────────────────────────────────────
  document.querySelectorAll('.filter-panel input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', () => {
      activeTypes = new Set(
        [...document.querySelectorAll('.filter-panel input[type=checkbox]')]
          .filter(el => el.checked)
          .map(el => el.dataset.type)
      );
      buildGraph();
    });
  });

  document.getElementById('graph-search').addEventListener('input', e => {
    searchTerm = e.target.value.trim().toLowerCase();
    buildGraph();
  });

  // ── Init ────────────────────────────────────────────────────────────────
  buildGraph();

  // Responsive resize
  window.addEventListener('resize', () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    svg.attr('width', w).attr('height', h);
    if (simulation) {
      simulation.force('center', d3.forceCenter(w / 2, h / 2)).alpha(0.3).restart();
    }
  });
})();
