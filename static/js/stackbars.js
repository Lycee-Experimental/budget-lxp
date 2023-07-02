//On récupère la valeur du budget prévisionnel
let data_max;
const dataPrevi = '/data?budget_previ=1';
fetch(dataPrevi)
    .then(response => response.json())
    .then(data => {
        data_max = d3.hierarchy(data).sum(d => d.value);
    });
// Définition de la fonction de création du diagramme Stackbars
const chart = rowdata => {
// On récupère les data pour en faire 
const data = d3.hierarchy(rowdata)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);

// Set up the chart dimensions and margins
const margin = { top: 20, right: 10, bottom: 30, left: 350 };
const container = document.getElementById('chart');
const width = container.clientWidth - margin.left - margin.right;
const height = container.clientHeight - margin.top - margin.bottom;
// Create an SVG element and append it to the chart container
console.log(width, height);
const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr("width", "100%")
    .attr("height", "100%");
const g =svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
// Set up the scales
const yScale = d3.scaleBand().range([0, height]).padding(0.3);
// Set the domains for the scales
yScale.domain(data.children.map((d) => d.data.name));
// Add the background bars
svg
    .selectAll(".background-bar")
    .data(data.children)
    .enter()
    .append("rect")
    .attr("class", "background-bar")
    .attr("x", 0)
    .attr("y", (d) => yScale(d.data.name))
    .attr("width", width)
    .attr("height", yScale.bandwidth());
// Add the bars
const bars = svg
    .selectAll(".bar")
    .data(data.children)
    .enter()
    .append("g")
    .attr("class", "bar")
    .attr("transform", (d) => `translate(0, ${yScale(d.data.name)})`);
bars
    .selectAll("rect")
    .data((d) => {
        let xPos = 0;
        const maxValueNode = data_max.descendants().find((node) => node.data.name === d.data.name);
        const maxValue = maxValueNode ? maxValueNode.value : 100000;
        console.log(maxValue, d.data.name);
        return d.children.map((child) => {
            const rectData = {
                ...child,
                x: xPos,
                width: (child.value / maxValue) * width,
            };
            xPos += rectData.width;
            return rectData;
        });
    })
    .enter()
    .append("rect")
    .attr("x", (d) => d.x)
    .attr("y", 0)
    .attr("width", (d) => d.width)
    .attr("height", yScale.bandwidth())
    .attr("fill", (d) => getColor(d))
    .on("mouseover", function (event, d) {
        // Show tooltip
        const tooltip = d3
            .select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("left", event.pageX + "px")
            .style("top", event.pageY + "px")
            .text(d.data.name);
    })
    .on("mouseout", function () {
        // Remove tooltip
        d3.select(".tooltip").remove();
    });
// Add labels for the categories
svg
    .selectAll(".category-label")
    .data(data.children)
    .enter()
    .append("text")
    .attr("class", "category-label")
    .attr("x", -10)
    .attr("y", (d) => yScale(d.data.name) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text((d) => d.data.name);
return svg.node();
};
// Function to assign a color to each subcategory
let parent;
let colorScale;
function getColor(d) {
    if (d.parent != parent) {
        parent = d.parent;
        const numberOfSiblings = d.parent ? d.parent.children.length : 0;
        colorScale = d3.scaleOrdinal()
        .range(d3.quantize(d3.interpolateRainbow, numberOfSiblings +1));
    }
    const subcategory = d.data.name;
  return colorScale(subcategory);
};
// Attente du chargement du document HTML
document.addEventListener("DOMContentLoaded", function (event) {
    // Obtention des paramètres GET reçus par la page
    const urlParams = new URLSearchParams(window.location.search);
    const params = urlParams.toString();
    // Renvoi des paramètres à la page /data
    const dataUrl = `/data?${params}`;
    // Récupération des données JSON pour le diagramme
    d3.json(dataUrl).then(data => {
        // Appel de la fonction de création du diagramme avec les données
        const chartContainer = document.getElementById('chart');
        chartContainer.appendChild(chart(data));
    });
});