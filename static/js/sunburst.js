// Définition de la fonction de création du diagramme Sunburst
const chart = (data, previ) => {
    const container = document.getElementById('chart');
    const clientWidth = container.clientWidth;
    const clientHeight = container.clientHeight;
    const width = Math.min(clientWidth, clientHeight)
    const radius = width / 7;

    // Configuration de l'arc pour le tracé des segments
    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
        .padRadius(radius * 1.5)
        .innerRadius(d => d.y0 * radius)
        .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

    // Fonction de partitionnement des données en hiérarchie
    const partition = data => {
        const root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);
        return d3.partition()
            .size([2 * Math.PI, root.height + 1])
            (root);
    };

    // Formatage des valeurs numériques avec un espace entre les milliers
    const format = (number) => {
        const formatter = d3.format(",.0f");
        const formattedValue = formatter(number);
        const replacedCommas = formattedValue.replace(",", " ");
        return replacedCommas;
    };

    // Création de la structure hiérarchique des données
    const root = partition(data);

    // Attribution des propriétés "current" à chaque élément de la hiérarchie
    root.each(d => d.current = d);

    // Création de l'élément SVG et du groupe principal
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, width])
        .style("font", "10px sans-serif");

    const g = svg.append("g")
        .attr("transform", `translate(${width / 2},${width / 2})`);

    // Première définition d'une échelle de couleurs pour les segments intérieurs du diagramme
    let color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, data.children.length + 1));

    // Définition de variables dans lesquelles on va stocker le niveau de hierarchie et le parent
    let depth = "";
    let monparent = "";

    // Tracé des segments du diagramme
    const path = g.append("g")
        .selectAll("path")
        .data(root.descendants().slice(1))
        .join("path")
        .attr("fill", d => {
            // Si on change de profondeur dans la hierarchie, ou que l'on change de parent,
            // On repart sur une nouvelle échelle de couleur
            if (d.depth != depth || d.parent != monparent) {
                depth = d.depth;
                monparent = d.parent;
                color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, d.parent.children.length + 1));
            };
            // On augmente la luminosité des couleurs en fonction du niveau de hierarchie
            return d3.color(color(d.data)).brighter(d.depth / 3);
        })
        .attr("fill-opacity", d => arcVisible(d.current) ? (d.children ? 1 : 0.6) : 0)
        .attr("pointer-events", d => arcVisible(d.current) ? "auto" : "none")
        .attr("d", d => arc(d.current));

    // Gestion des événements sur les segments
    path.filter(d => d.children)
        .style("cursor", "pointer")
        .on("click", clicked);

    // Ajout des infobulles sur les segments
    path.on("mouseover", function (event, d) {
        const ancestors = d.ancestors().map(d => d.data.name).reverse();
        const list = ['Domaine', 'Activité', 'Compte', 'Fournisseur', 'Détail'];
        let html = '';
        for (let i = 1; i < ancestors.length; i++) {
            html += `<tr><th>${list[i - 1]}</th><td>${ancestors[i]}<td><tr>`
        };
        d.data.date && (html += `<tr><th>Date</th><td>${d.data.date}<td><tr>`);
        html += `<tr><th>Montant</th><td>${format(d.value)} €<td><tr>`;
        tooltip.html(`<table>${html}</table>`)
            .style("visibility", "visible");

        // Update tooltip position on mouseover
        tooltip.style("top", event.pageY + "px")
            .style("left", event.pageX + "px");
    })
        .on("mousemove", function (event) {
            // Update tooltip position on mousemove
            tooltip.style("top", (event.pageY - 10) + "px")
                .style("left", (event.pageX + 10) + "px");
        })
        .on("mouseout", function () {
            tooltip.style("visibility", "hidden");
        });

    // Ajout des étiquettes du diagramme
    const label = g.append("g")
        .attr("pointer-events", "none")
        .attr("text-anchor", "middle")
        .style("user-select", "none")
        .selectAll("text")
        .data(root.descendants().slice(1))
        .join("text")
        .attr("dy", "0.35em")
        .attr("fill-opacity", d => +labelVisible(d.current))
        .attr("transform", d => labelTransform(d.current))
        .text(d => d.data.name);

    // Ajout du cercle central pour la navigation
    const parent = g.append("circle")
        .datum(root)
        .attr("r", radius)
        .attr("fill", "none")
        .attr("pointer-events", "all")
        .on("click", clicked);

    //Ajouter des tooltips
    var tooltip = d3.select("body")
        .append("div")
        .attr("id", "tooltip")

    // Fonction de gestion de l'événement de clic sur un segment
    function clicked(event, p) {
        parent.datum(p.parent || root);
        root.each(d => d.target = {
            x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
            x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
            y0: Math.max(0, d.y0 - p.depth),
            y1: Math.max(0, d.y1 - p.depth)
        });
        const t = g.transition().duration(750);
        path.transition(t)
            .tween("data", d => {
                const i = d3.interpolate(d.current, d.target);
                return t => d.current = i(t);
            })
            .filter(function (d) {
                return +this.getAttribute("fill-opacity") || arcVisible(d.target);
            })
            .attr("fill-opacity", d => arcVisible(d.target) ? (d.children ? 1 : 0.6) : 0)
            .attr("pointer-events", d => arcVisible(d.target) ? "auto" : "none")
            .attrTween("d", d => () => arc(d.current));

        label.filter(function (d) {
            return +this.getAttribute("fill-opacity") || labelVisible(d.target);
        }).transition(t)
            .attr("fill-opacity", d => +labelVisible(d.target))
            .attrTween("transform", d => () => labelTransform(d.current));

        //Mise à jour des informations de navigation
        if (!previ) {showInfo(p)};
        pourcentage(p);
        pourcentage_total(p);
    }

    //Affichage des informations de navigation
    function showInfo(data) {
        // On affiche l'info
        var card = d3.select("#informations");
        card.style("visibility", "visible");
        // On traite les données
        const ancestors = data.ancestors().map(data => data.data.name).reverse();
        const list = ['Domaine', 'Activité', 'Compte', 'Fournisseur', 'Détail'];
        // On les met en forme de tableau
        let html = '';
        for (let i = 1; i < ancestors.length; i++) {
            html += `<tr><th>${list[i - 1]}</th><td> : ${ancestors[i]}<td><tr>`
        };
        data.data.date && (html += `<tr><th>Date</th><td> : ${data.data.date}<td><tr>`);
        html += `<tr><th>Montant</th><td> : ${format(data.value)} €<td><tr>`;
        // On affiche le tableau dans le #info
        var info = d3.select("#info");
        info.html(`<table>${html}</table>`)
            .style("visibility", "visible");
    };

    //On prend la valeur du budget prévisionnel
    let budgetPrevi;
    const dataPrevi = '/data?budget_previ=1';
    fetch(dataPrevi)
        .then(response => response.json())
        .then(data => {
            budgetPrevi = d3.hierarchy(data).sum(d => d.value);
            // Appelle la fonction "pourcentage" après que fetch(dataPrevi)
            pourcentage_total(root);
        });


    if (!previ) {showInfo(root)};    


    //Affichage des informations de navigation
    function showInfo(data) {
        // On affiche l'info
        var card = d3.select("#informations");
        card.style("visibility", "visible");
        // On traite les données
        const ancestors = data.ancestors().map(data => data.data.name).reverse();
        const list = ['Domaine', 'Activité', 'Compte', 'Fournisseur', 'Détail'];
        // On les met en forme de tableau
        let html = '';
        for (let i = 1; i < ancestors.length; i++) {
            html += `<tr><th>${list[i - 1]}</th><td> : ${ancestors[i]}<td><tr>`
        };
        data.data.date && (html += `<tr><th>Date</th><td> : ${data.data.date}<td><tr>`);
        html += `<tr><th>Montant</th><td> : ${format(data.value)} €<td><tr>`;
        // On affiche le tableau dans le #info
        var info = d3.select("#info");
        info.html(`<table>${html}</table>`)
            .style("visibility", "visible");
    };

    let nom_domaine2;   
    // Pourcentage du budget dépensé 
    function pourcentage(d) {
        let nom_domaine = d.data.name;
        const node = budgetPrevi.descendants().find(d => d.data.name === nom_domaine);
        if (node) {
          budget = node.value;
          nom_domaine2 = node.data.name;
        } 
        console.log(nom_domaine, nom_domaine2)
        const pourcentage_budget = d.value * 100 / budget;
        const couleur_pourcentage=get_color(pourcentage_budget);
        var pourcentage = d3.select('#pourcentage');
        pourcentage.html(`<progress class="progress ${couleur_pourcentage}" value="${pourcentage_budget.toFixed(1)}" max="100"><p class="subtitle"></p></progress>
    <center><strong>${pourcentage_budget.toFixed(1)} %</strong> des ${format(budget)} € de <strong>${nom_domaine2 || "annuel avec Travaux"}</strong> </center>`);
    }

    // Pourcentage du budget dépensé total
    function pourcentage_total(d) {
        
        const budget_total = budgetPrevi.value - budgetPrevi.descendants().find(d => d.data.name === "Travaux").value;
        const pourcentage_budget = d.value * 100 / budget_total;
        const pourcentage_tot = d3.select('#pourcentage_tot');
        
        const couleur_pourcentage = get_color(pourcentage_budget);
        
        pourcentage_tot.html(`<progress class="progress ${couleur_pourcentage}" value="${pourcentage_budget.toFixed(1)}" max="100"><p class="subtitle"></p></progress>
                <center><strong>${pourcentage_budget.toFixed(1)} %</strong> des ${format(budget_total)} € de <strong>budget annuel</strong></center>`);
    }

    // Fonction pour déterminer la couleur de la barre de jauge
    function get_color(percent) {
        const conditions = [
            { min: 80, classe: "is-danger" },
            { min: 60, classe: "is-warning" },
            { min: 40, classe: "is-primary" },
            { min: 0, classe: "is-success" }
        ];
        for (var i = 0; i < conditions.length; i++) {
            if (percent > conditions[i].min) {
                return conditions[i].classe;
            }
        }
    }

    // Fonction pour déterminer la visibilité d'un segment
    function arcVisible(d) {
        return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
    }

    // Fonction pour déterminer la visibilité d'une étiquette
    function labelVisible(d) {
        return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
    }

    // Fonction pour transformer la position d'une étiquette
    function labelTransform(d) {
        const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
        const y = (d.y0 + d.y1) / 2 * radius;
        return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
    }
    console.log(svg.node());

    return svg.node();
};

// Attente du chargement du document HTML
document.addEventListener("DOMContentLoaded", function (event) {
    // Obtention des paramètres GET reçus par la page
    const urlParams = new URLSearchParams(window.location.search);
    const params = urlParams.toString();
    const previ = urlParams.has('budget_previ');
    // Renvoi des paramètres à la page /data
    const dataUrl = `/data?${params}`;
    // Récupération des données JSON pour le diagramme
    d3.json(dataUrl).then(data => {
        // Appel de la fonction de création du diagramme avec les données
        const chartContainer = document.getElementById('chart');
        chartContainer.appendChild(chart(data, previ));
    }).catch(error => {
        console.log(error);
    });
});