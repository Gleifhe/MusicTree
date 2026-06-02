/**
 * MusicTree — Full D3 Force-Directed Graph (Homepage)
 * Uses global GRAPH_DATA injected by Hugo template.
 */
(function () {
  // HTML-escape untrusted strings before inserting into innerHTML.
  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  }

  // Only allow same-origin relative paths and https:// URLs.
  function safeUrl(u) {
    if (!u) return '#';
    if (/^https?:\/\//i.test(u)) return u;
    if (/^\/[^/]/i.test(u) || u === '/') return u;
    return '#';
  }
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

  let allNodes = [];
  let allLinks = [];

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

  // Called once after data loads — builds full graph for ALL nodes/links.
  function buildGraph() {
    // Use all nodes; applyFilter() handles show/hide after build.
    const nodeData = allNodes.map(d => ({ ...d }));
    const linkData = allLinks.map(d => ({
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
      .filter(([, nodes]) => nodes.length >= 1)
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
          if (d.url) window.location.href = safeUrl(d.url);
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

    // ── Scene clustering force ────────────────────────────────────────────
    // Assign fixed scene "home" positions arranged in a circle around center
    const sceneNames = [...new Set(artistNodes.map(n => n.scene).filter(Boolean))];
    const sceneAngle = {};
    sceneNames.forEach((s, i) => {
      sceneAngle[s] = (i / sceneNames.length) * 2 * Math.PI;
    });
    const clusterRadius = Math.min(width, height) * 0.32;
    const sceneCenters = {};
    sceneNames.forEach(s => {
      sceneCenters[s] = {
        x: width  / 2 + clusterRadius * Math.cos(sceneAngle[s]),
        y: height / 2 + clusterRadius * Math.sin(sceneAngle[s]),
      };
    });

    // Seed initial positions near scene center so simulation converges faster
    nodeData.forEach(n => {
      const sc = n.scene && sceneCenters[n.scene];
      if (sc && !n.x) {
        n.x = sc.x + (Math.random() - 0.5) * 80;
        n.y = sc.y + (Math.random() - 0.5) * 80;
      }
    });

    function sceneClusterForce(alpha) {
      const strength = 0.12 * alpha;
      nodeData.forEach(n => {
        if (n.type === 'artist' && n.scene && sceneCenters[n.scene]) {
          n.vx += (sceneCenters[n.scene].x - n.x) * strength;
          n.vy += (sceneCenters[n.scene].y - n.y) * strength;
        }
      });
    }

    let posById = {};
    simulation = d3.forceSimulation(nodeData)
      .force('link', d3.forceLink(linkData).id(d => d.id).distance(d => {
        return d.relation === 'appears-on' ? 60 : 90;
      }))
      .force('charge', d3.forceManyBody().strength(-180).distanceMax(300).theta(0.9))
      .force('center', d3.forceCenter(width / 2, height / 2).strength(0.05))
      .force('collision', d3.forceCollide().radius(d => (NODE_RADIUS[d.type] || 12) + 14))
      .force('sceneCluster', sceneClusterForce)
      .alphaDecay(0.03)
      .velocityDecay(0.4)
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
        gArtistLabels.selectAll('text')
          .attr('x', d => { const n = posById[d.id]; return n ? n.x : 0; })
          .attr('y', d => { const n = posById[d.id]; return n ? n.y + 24 : 0; });

        // Move scene labels to the scene's fixed cluster center
        gSceneLabels.selectAll('text')
          .attr('x', d => sceneCenters[d.scene] ? sceneCenters[d.scene].x : 0)
          .attr('y', d => sceneCenters[d.scene] ? sceneCenters[d.scene].y : 0);
      });

    // Build posById once so the tick handler doesn't rebuild it every frame
    nodeData.forEach(n => { posById[n.id] = n; });

    // Stop simulation after 8s to prevent runaway CPU usage
    setTimeout(() => simulation && simulation.stop(), 8000);
  }

  // Called on filter/search changes — just show/hide existing DOM elements.
  function applyFilter() {
    const visibleIds = new Set(
      allNodes
        .filter(n => activeTypes.has(n.type) && (!searchTerm || n.label.toLowerCase().includes(searchTerm)))
        .map(n => n.id)
    );
    if (nodeEls) {
      nodeEls.style('display', d => visibleIds.has(d.id) ? null : 'none');
    }
    if (linkEls) {
      linkEls.style('display', d => {
        const s = typeof d.source === 'object' ? d.source.id : d.source;
        const t = typeof d.target === 'object' ? d.target.id : d.target;
        return visibleIds.has(s) && visibleIds.has(t) ? null : 'none';
      });
    }
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
      <div class="tooltip-type">${esc(d.type)}</div>
      <div class="tooltip-title">${esc(d.label)}</div>
      ${d.meta ? `<div style="font-size:0.78rem;color:#8888aa;margin-top:0.2rem">${esc(d.meta)}</div>` : ''}
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

  // ── Fetch data, then wire everything up ─────────────────────────────────
  const graphUrl = container.dataset.graphUrl || '/data/graph-slim.json';
  fetch(graphUrl)
    .then(r => r.json())
    .then(rawData => {
      document.getElementById('graph-loading')?.remove();
      allNodes = rawData.nodes.map(d => ({ ...d }));
      allLinks = rawData.links.map(d => ({ ...d }));
      buildGraph();

      document.getElementById('btn-random')?.addEventListener('click', () => {
        const artists = allNodes.filter(n => n.type === 'artist');
        if (artists.length && artists[0].url) {
          const pick = artists[Math.floor(Math.random() * artists.length)];
          window.location.href = safeUrl(pick.url);
        }
      });

      // ── Filters ───────────────────────────────────────────────────────
      document.querySelectorAll('.filter-panel input[type=checkbox]').forEach(cb => {
        cb.addEventListener('change', () => {
          activeTypes = new Set(
            [...document.querySelectorAll('.filter-panel input[type=checkbox]')]
              .filter(el => el.checked)
              .map(el => el.dataset.type)
          );
          applyFilter();
          // Light restart so newly-visible nodes settle into position
          if (simulation) simulation.alpha(0.15).restart();
        });
      });

      // ── Search ────────────────────────────────────────────────────────
      const suggestions = document.getElementById('search-suggestions');
      document.getElementById('graph-search').addEventListener('input', e => {
        searchTerm = e.target.value.trim().toLowerCase();
        applyFilter();
        if (suggestions && searchTerm.length >= 2) {
          const matches = allNodes
            .filter(n => n.label.toLowerCase().includes(searchTerm))
            .sort((a, b) => {
              const order = { artist: 0, person: 1, album: 2, song: 3 };
              return (order[a.type] || 9) - (order[b.type] || 9);
            })
            .slice(0, 8);
          if (matches.length) {
            suggestions.innerHTML = matches.map(n =>
              `<a href="${esc(safeUrl(n.url))}" class="suggestion-item suggestion-${esc(n.type)}">
                <span class="suggestion-type">${esc(n.type)}</span>
                <span class="suggestion-label">${esc(n.label)}</span>
              </a>`
            ).join('');
            suggestions.style.display = 'block';
          } else {
            suggestions.style.display = 'none';
          }
        } else if (suggestions) {
          suggestions.style.display = 'none';
        }
      });

      document.getElementById('graph-search').addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          const term = e.target.value.trim().toLowerCase();
          const matches = allNodes.filter(n => n.label.toLowerCase().includes(term));
          if (matches.length === 1 && matches[0].url) {
            window.location.href = safeUrl(matches[0].url);
          } else if (matches.length > 0) {
            const artistMatch = matches.find(n => n.type === 'artist');
            const best = artistMatch || matches[0];
            if (best.url) window.location.href = safeUrl(best.url);
          }
        }
      });

      document.addEventListener('click', e => {
        if (suggestions && !e.target.closest('.search-panel')) {
          suggestions.style.display = 'none';
        }
      });

      // ── Path Finder ───────────────────────────────────────────────────
      function findPath(fromId, toId) {
        if (fromId === toId) return [fromId];
        const adj = {};
        allLinks.forEach(l => {
          const s = typeof l.source === 'object' ? l.source.id : l.source;
          const t = typeof l.target === 'object' ? l.target.id : l.target;
          (adj[s] = adj[s] || []).push(t);
          (adj[t] = adj[t] || []).push(s);
        });
        const prev = { [fromId]: null };
        const queue = [fromId];
        while (queue.length) {
          const cur = queue.shift();
          if (cur === toId) {
            const path = [];
            let node = toId;
            while (node !== null) { path.unshift(node); node = prev[node]; }
            return path;
          }
          for (const nb of (adj[cur] || [])) {
            if (!(nb in prev)) { prev[nb] = cur; queue.push(nb); }
          }
        }
        return null;
      }

      function nodeById(id) { return allNodes.find(n => n.id === id); }

      function setupPathFinder() {
        const fromInput = document.getElementById('path-from');
        const toInput   = document.getElementById('path-to');
        const btn       = document.getElementById('btn-find-path');
        const result    = document.getElementById('path-result');
        if (!btn) return;

        function makeAutocomplete(input) {
          const dropdown = document.createElement('div');
          dropdown.className = 'search-suggestions';
          dropdown.style.minWidth = '200px';
          input.parentNode.style.position = 'relative';
          input.insertAdjacentElement('afterend', dropdown);
          input.addEventListener('input', () => {
            const q = input.value.trim().toLowerCase();
            if (q.length < 2) { dropdown.style.display = 'none'; return; }
            const matches = allNodes
              .filter(n => (n.type === 'artist' || n.type === 'person') && n.label.toLowerCase().includes(q))
              .slice(0, 6);
            if (!matches.length) { dropdown.style.display = 'none'; return; }
            dropdown.innerHTML = matches.map(n =>
              `<div class="suggestion-item suggestion-${esc(n.type)}" data-id="${esc(n.id)}" data-label="${esc(n.label)}" style="cursor:pointer">
                <span class="suggestion-type">${esc(n.type)}</span>
                <span class="suggestion-label">${esc(n.label)}</span>
              </div>`
            ).join('');
            dropdown.style.display = 'block';
            dropdown.querySelectorAll('[data-id]').forEach(el => {
              el.addEventListener('click', () => {
                input.value = el.dataset.label;
                input.dataset.selectedId = el.dataset.id;
                dropdown.style.display = 'none';
              });
            });
          });
        }

        makeAutocomplete(fromInput);
        makeAutocomplete(toInput);

        btn.addEventListener('click', () => {
          const fromId = fromInput.dataset.selectedId ||
            (allNodes.find(n => n.label.toLowerCase() === fromInput.value.toLowerCase()) || {}).id;
          const toId = toInput.dataset.selectedId ||
            (allNodes.find(n => n.label.toLowerCase() === toInput.value.toLowerCase()) || {}).id;
          if (!fromId || !toId) {
            result.innerHTML = '<span style="color:#e15759">Could not find one or both names. Try selecting from the dropdown.</span>';
            return;
          }
          const path = findPath(fromId, toId);
          if (!path) {
            result.innerHTML = '<span style="color:#e15759">No connection found between these two.</span>';
            return;
          }
          const steps = path.map(id => {
            const n = nodeById(id);
            return n ? `<a href="${esc(safeUrl(n.url))}" class="path-node path-node-${esc(n.type)}">${esc(n.label)}</a>` : esc(id);
          }).join('<span class="path-sep"> → </span>');
          result.innerHTML = `<div class="path-steps"><strong>${esc(String(path.length - 1))} degree${path.length - 1 !== 1 ? 's' : ''} of separation</strong><br><div class="path-chain">${steps}</div></div>`;
        });
      }
      setupPathFinder();
    })
    .catch(err => {
      console.error('MusicTree: failed to load graph-slim.json', err);
      const loading = document.getElementById('graph-loading');
      if (loading) loading.textContent = '⚠ Could not load graph data. Try refreshing.';
    });

  // ── Responsive resize ────────────────────────────────────────────────────
  window.addEventListener('resize', () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    svg.attr('width', w).attr('height', h);
    if (simulation) {
      simulation.force('center', d3.forceCenter(w / 2, h / 2)).alpha(0.3).restart();
    }
  });
})();
