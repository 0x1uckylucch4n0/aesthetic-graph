// ── Graph setup ──
const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("#graph")
  .attr("viewBox", [0, 0, width, height])
  .attr("preserveAspectRatio", "xMidYMid meet");

const container = svg.append("g");

// ── Zoom ──
const zoom = d3.zoom()
  .scaleExtent([0.05, 4])
  .on("zoom", (e) => container.attr("transform", e.transform));

svg.call(zoom);

// Center the initial view — zoom out more for large graphs
const initialScale = aesthetics.length > 200 ? 0.25 : aesthetics.length > 50 ? 0.45 : 0.75;
svg.call(zoom.transform, d3.zoomIdentity.translate(width / 2, height / 2).scale(initialScale));

// ── Build node/link data ──
const nodeData = aesthetics.map(a => ({ ...a }));
const nodeMap = new Map(nodeData.map(n => [n.id, n]));

// Only include connections where both source and target exist
const linkData = connections
  .filter(c => nodeMap.has(c.source) && nodeMap.has(c.target))
  .map(c => ({
    source: c.source,
    target: c.target,
    label: c.label || ""
  }));

// ── Force simulation ──
// Tune forces for graph size
const nodeCount = nodeData.length;
const chargeStrength = nodeCount > 500 ? -200 : nodeCount > 100 ? -400 : -700;
const linkDist = nodeCount > 500 ? 120 : nodeCount > 100 ? 180 : 260;
const collisionRadius = nodeCount > 500 ? 40 : nodeCount > 100 ? 60 : 100;

const simulation = d3.forceSimulation(nodeData)
  .force("link", d3.forceLink(linkData).id(d => d.id).distance(linkDist))
  .force("charge", d3.forceManyBody().strength(chargeStrength))
  .force("collision", d3.forceCollide().radius(d => {
    const s = (typeof STAR_SIZES !== 'undefined' && STAR_SIZES[d.size])
      ? STAR_SIZES[d.size].outer : 55;
    return s + 10;
  }))
  .force("x", d3.forceX(0).strength(0.03))
  .force("y", d3.forceY(0).strength(0.03));

// Pre-compute so graph appears settled
const preTicks = nodeCount > 500 ? 500 : nodeCount > 100 ? 400 : 350;
simulation.tick(preTicks);
simulation.alpha(0.05).restart();

// ── Draw edges ──
const linkGroup = container.append("g").attr("class", "links");

const links = linkGroup.selectAll("g")
  .data(linkData)
  .join("g")
  .attr("class", "link-group");

links.append("path")
  .attr("class", "link-line")
  .attr("id", (d, i) => `link-${i}`);

links.append("text")
  .attr("class", "link-label")
  .attr("dy", -6)
  .append("textPath")
  .attr("href", (d, i) => `#link-${i}`)
  .attr("startOffset", "50%")
  .attr("text-anchor", "middle")
  .text(d => d.label);

// ── Fat rounded star path generator ──
function fatStarPath(outerR, innerR, rounding) {
  const points = [];
  for (let i = 0; i < 5; i++) {
    const outerAngle = (i * 2 * Math.PI / 5) - Math.PI / 2;
    points.push([
      Math.cos(outerAngle) * outerR,
      Math.sin(outerAngle) * outerR
    ]);
    const innerAngle = outerAngle + Math.PI / 5;
    points.push([
      Math.cos(innerAngle) * innerR,
      Math.sin(innerAngle) * innerR
    ]);
  }

  let d = "";
  const n = points.length;
  for (let i = 0; i < n; i++) {
    const curr = points[i];
    const next = points[(i + 1) % n];
    const prev = points[(i - 1 + n) % n];

    const dx1 = prev[0] - curr[0], dy1 = prev[1] - curr[1];
    const dx2 = next[0] - curr[0], dy2 = next[1] - curr[1];
    const len1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
    const len2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);

    const r = Math.min(rounding, len1 / 2, len2 / 2);
    const startX = curr[0] + (dx1 / len1) * r;
    const startY = curr[1] + (dy1 / len1) * r;
    const endX = curr[0] + (dx2 / len2) * r;
    const endY = curr[1] + (dy2 / len2) * r;

    if (i === 0) {
      d += `M${startX},${startY}`;
    } else {
      d += `L${startX},${startY}`;
    }
    d += `Q${curr[0]},${curr[1]} ${endX},${endY}`;
  }
  d += "Z";
  return d;
}

// ── Get star dimensions for a node ──
function getStarParams(d) {
  if (typeof STAR_SIZES !== 'undefined' && STAR_SIZES[d.size]) {
    const s = STAR_SIZES[d.size];
    return { outer: s.outer, inner: s.inner, round: s.round };
  }
  return { outer: 55, inner: 34, round: 11 }; // default medium
}

// ── Draw nodes ──
const nodeGroup = container.append("g").attr("class", "nodes");

const nodes = nodeGroup.selectAll("g")
  .data(nodeData)
  .join("g")
  .attr("class", "node-group")
  .call(drag(simulation));

nodes.append("path")
  .attr("class", "node-star")
  .attr("d", d => {
    const p = getStarParams(d);
    return fatStarPath(p.outer, p.inner, p.round);
  })
  .attr("fill", d => FAMILIES[d.family]?.color || "#eee")
  .attr("stroke", d => FAMILIES[d.family]?.stroke || "#ccc");

nodes.append("text")
  .attr("class", "node-label")
  .attr("y", -4)
  .style("font-size", d => {
    const sizes = { 1: "10px", 2: "12px", 3: "15px", 4: "17px", 5: "20px" };
    return sizes[d.size] || "15px";
  })
  .text(d => d.name);

nodes.append("text")
  .attr("class", "node-family")
  .attr("y", d => {
    const offsets = { 1: 8, 2: 10, 3: 14, 4: 16, 5: 18 };
    return offsets[d.size] || 14;
  })
  .style("font-size", d => d.size <= 2 ? "7px" : "9px")
  .text(d => d.family);

// ── Hover behavior ──
const connectedNodes = new Map();
nodeData.forEach(n => connectedNodes.set(n.id, new Set()));
linkData.forEach(l => {
  const sid = typeof l.source === "object" ? l.source.id : l.source;
  const tid = typeof l.target === "object" ? l.target.id : l.target;
  if (connectedNodes.has(sid)) connectedNodes.get(sid).add(tid);
  if (connectedNodes.has(tid)) connectedNodes.get(tid).add(sid);
});

nodes.on("mouseenter", function(event, d) {
  const connected = connectedNodes.get(d.id);

  nodes.classed("dimmed", n => n.id !== d.id && !connected.has(n.id));
  nodes.classed("highlighted", n => n.id === d.id || connected.has(n.id));

  links.classed("dimmed", l => {
    const sid = typeof l.source === "object" ? l.source.id : l.source;
    const tid = typeof l.target === "object" ? l.target.id : l.target;
    return sid !== d.id && tid !== d.id;
  });
  links.classed("highlighted", l => {
    const sid = typeof l.source === "object" ? l.source.id : l.source;
    const tid = typeof l.target === "object" ? l.target.id : l.target;
    return sid === d.id || tid === d.id;
  });
});

nodes.on("mouseleave", function() {
  nodes.classed("dimmed", false).classed("highlighted", false);
  links.classed("dimmed", false).classed("highlighted", false);
});

// ── Click behavior ──
nodes.on("click", function(event, d) {
  event.stopPropagation();
  openPanel(d);
});

svg.on("click", () => closePanel());

// ── Tick ──
simulation.on("tick", () => {
  links.select("path")
    .attr("d", d => {
      const dx = d.target.x - d.source.x;
      const dy = d.target.y - d.source.y;
      const dr = Math.sqrt(dx * dx + dy * dy) * 1.2;
      return `M${d.source.x},${d.source.y}A${dr},${dr} 0 0,1 ${d.target.x},${d.target.y}`;
    });

  nodes.attr("transform", d => `translate(${d.x},${d.y})`);
});

// ── Drag ──
function drag(sim) {
  return d3.drag()
    .on("start", (event, d) => {
      if (!event.active) sim.alphaTarget(0.1).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on("drag", (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on("end", (event, d) => {
      if (!event.active) sim.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    });
}

// ── Keyboard ──
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closePanel();
});

// ── Expose for panel ──
function navigateToNode(id) {
  const node = nodeData.find(n => n.id === id);
  if (node) openPanel(node);
}
