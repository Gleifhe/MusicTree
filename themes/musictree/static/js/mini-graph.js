/**
 * MusicTree — Mini D3 Graph for individual content pages.
 * Loads graph.json via fetch (cached), then renders the full connected
 * neighbourhood of FOCUS_NODE — prioritising close hops, capped at MAX_NODES.
 */
(function () {
  const NODE_COLORS = {
    artist: '#4e79a7',
    person: '#59a14f',
    album:  '#b07aa1',
    song:   '#f28e2b',
  };
  const NODE_RADIUS = { artist: 16, person: 12, album: 13, song: 9 };

  const focusId   = window.FOCUS_NODE;
  const container = document.getElementById('mini-graph');
  if (!container || !focusId) return;

  // Fetch graph data from static file (browser caches it across pages)
  fetch('/data/graph-slim.json')
    .then(r => r.json())
    .then(rawData => renderGraph(rawData))
    .catch(err => console.error('MusicTree: failed to load graph-slim.json', err));

  function renderGraph(rawData) {
    if (!rawData.nodes || !rawData.nodes.length) return;

  // Helper: normalise source/target to string id
  function sid(v) { return typeof v === 'object' ? v.id : v; }

  // Build adjacency for fast lookup
  const adj = {};
  rawData.links.forEach(l => {
    const s = sid(l.source), t = sid(l.target);
    (adj[s] = adj[s] || []).push({ id: t, rel: l.relation });
    (adj[t] = adj[t] || []).push({ id: s, rel: l.relation });
  });

  // BFS — full traversal but cap at MAX_NODES, prioritising lower hop counts.
  // Fills hop-by-hop so close neighbours are always included before distant ones.
  const MAX_NODES = 80;
  const visited = new Map(); // id → hop distance
  const queue = [[focusId, 0]];
  visited.set(focusId, 0);

  while (queue.length && visited.size < MAX_NODES) {
    const [id, dist] = queue.shift();
    (adj[id] || []).forEach(({ id: nid }) => {
      if (!visited.has(nid)) {
        visited.set(nid, dist + 1);
        queue.push([nid, dist + 1]);
      }
    });
  }

  const neighbourIds = new Set(visited.keys());

  const nodeData = rawData.nodes
    .filter(n => neighbourIds.has(n.id))
    .map(d => ({ ...d, _hop: visited.get(d.id) }));

  const nodeIds = new Set(nodeData.map(n => n.id));
  const linkData = rawData.links
    .filter(l => nodeIds.has(sid(l.source)) && nodeIds.has(sid(l.target)))
    .map(d => ({
      source:   sid(d.source),
      target:   sid(d.target),
      relation: d.relation,
    }));

  const W = container.clientWidth  || 560;
  const H = container.clientHeight || 320;

  const svg = d3.select(container).append('svg')
    .attr('width', W).attr('height', H);

  const gRoot = svg.append('g');
  svg.call(d3.zoom().scaleExtent([0.2, 4]).on('zoom', e => gRoot.attr('transform', e.transform)));

  // Link colour by relation type
  function linkColor(rel) {
    if (rel === 'member-of')    return '#4e79a7';
    if (rel === 'released')     return '#b07aa1';
    if (rel === 'appears-on')   return '#f28e2b';
    if (rel === 'performed-by') return '#59a14f';
    if (rel === 'produced-by')  return '#e15759';
    if (rel === 'written-by')   return '#f28e2b';
    return '#444466';
  }

  // Links
  const linkEls = gRoot.append('g').selectAll('line')
    .data(linkData)
    .join('line')
      .attr('stroke', d => linkColor(d.relation))
      .attr('stroke-width', 1.5)
      .attr('stroke-opacity', 0.6);

  // Link relation labels (only show on 1-hop links to keep it readable)
  const RELATION_SHORT = {
    'member-of':    'member',
    'released':     'released',
    'appears-on':   'on',
    'performed-by': 'performed',
    'produced-by':  'produced',
    'written-by':   'wrote',
    'played':       'played',
  };

  const linkLabelEls = gRoot.append('g').selectAll('text')
    .data(linkData.filter(l => {
      return sid(l.source) === focusId || sid(l.target) === focusId;
    }))
    .join('text')
      .attr('fill', '#8888aa')
      .attr('font-size', 9)
      .attr('text-anchor', 'middle')
      .attr('pointer-events', 'none')
      .text(d => RELATION_SHORT[d.relation] || d.relation || '');

  // Nodes
  const gNode = gRoot.append('g').selectAll('g')
    .data(nodeData, d => d.id)
    .join('g')
      .attr('cursor', d => d.url ? 'pointer' : 'default')
      .on('click', (event, d) => { if (d.url) window.open(d.url, '_blank', 'noopener'); });

  // Tooltip
  const tip = d3.select(container).append('div')
    .style('position', 'absolute')
    .style('background', '#1a1a24')
    .style('border', '1px solid #333350')
    .style('border-radius', '6px')
    .style('padding', '0.4rem 0.7rem')
    .style('font-size', '12px')
    .style('pointer-events', 'none')
    .style('color', '#e8e8f0')
    .style('display', 'none')
    .style('z-index', '20');

  gNode
    .on('mouseover', (event, d) => {
      tip.style('display', 'block')
         .html(`<strong>${d.label}</strong><br><span style="color:#8888aa;font-size:10px">${d.type}${d.meta ? ' · ' + d.meta : ''}</span>`);
    })
    .on('mousemove', (event) => {
      const rect = container.getBoundingClientRect();
      tip.style('left',  (event.clientX - rect.left + 10) + 'px')
         .style('top',   (event.clientY - rect.top  + 10) + 'px');
    })
    .on('mouseout', () => tip.style('display', 'none'));

  gNode.append('circle')
    .attr('r', d => d.id === focusId ? (NODE_RADIUS[d.type] || 12) + 5 : NODE_RADIUS[d.type] || 12)
    .attr('fill', d => NODE_COLORS[d.type] || '#888')
    .attr('stroke', d => d.id === focusId ? '#ffffff' : d._hop <= 1 ? d3.color(NODE_COLORS[d.type] || '#888').brighter(0.4) : 'transparent')
    .attr('stroke-width', d => d.id === focusId ? 3 : 1.5)
    .attr('opacity', d => d._hop === 0 ? 1 : Math.max(0.3, 1 - d._hop * 0.18));

  gNode.append('text')
    .attr('dy', d => -(NODE_RADIUS[d.type] || 12) - 4)
    .attr('text-anchor', 'middle')
    .attr('fill', '#e8e8f0')
    .attr('font-size', d => d.id === focusId ? 12 : 10)
    .attr('font-weight', d => d.id === focusId ? 700 : 400)
    .attr('pointer-events', 'none')
    .style('text-shadow', '0 1px 3px rgba(0,0,0,0.9)')
    .text(d => d.label.length > 20 ? d.label.slice(0, 18) + '…' : d.label);

  // Distance-based link lengths: closer for direct connections, longer for 2-hop
  function linkDist(d) {
    const sFocused = sid(d.source) === focusId || sid(d.target) === focusId;
    if (sFocused) return 100;
    if (d.relation === 'appears-on') return 60;
    return 90;
  }

  const sim = d3.forceSimulation(nodeData)
    .force('link', d3.forceLink(linkData).id(d => d.id).distance(linkDist))
    .force('charge', d3.forceManyBody().strength(d => d.id === focusId ? -300 : -80))
    .force('center', d3.forceCenter(W / 2, H / 2))
    .force('collision', d3.forceCollide().radius(d => (NODE_RADIUS[d.type] || 12) + 14))
    .alphaDecay(0.04)
    .on('tick', () => {
      linkEls
        .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);

      linkLabelEls
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2);

      gNode.attr('transform', d => `translate(${d.x},${d.y})`);
    });

  // Stop simulation after 4 seconds to prevent runaway CPU
  setTimeout(() => sim.stop(), 4000);

  // Pin focus node to center initially then release
  const focus = nodeData.find(n => n.id === focusId);
  if (focus) { focus.fx = W / 2; focus.fy = H / 2; }
  setTimeout(() => { if (focus) { focus.fx = null; focus.fy = null; } }, 1500);
  } // end renderGraph
})();

