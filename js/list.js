// Immediately Invoked Function Expression to limit access to our 
// variables

//Renders the table of Hive data
function chart(data) {

    let columns = Object.keys(data[0])

    let table = d3.select('#vertical-menu').append('table')
    let thead = table.append('thead')
    let tbody = table.append('tbody')

    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function (d) { return d })

    let rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr')

    let cells = rows.selectAll('td')
        .data(function(row) {
            return columns.map(function (column) {
                return { column: column, value: row[column] }
            })
        })
        .enter()
    .append('td')
        .text(function (d) { return d.value })

    // Add interactivity
    rows.on("mousedown", (d, i, elements) => {
        d3.select("tr.selected").classed("selected", false)
        d3.select(elements[i]).classed("selected", true)
        update(d['Hive ID'], d['Health'], d['City'])
        highlightMap([d['Hive ID']], "selected", markPoint)
    }).on("mouseover", (d, i, elements) => {
        d3.select(elements[i]).classed("mouseover", true)
    }).on("mouseout", (d, i, elements) => {
        d3.select(elements[i]).classed("mouseover", false)
    });

    return table;
}

//Loads Hive, City, Health data.
d3.csv("data/ids_cities_health.csv", function(data) {
    chart(data)
});

//Marks the corresponing points on the map with a given class and marking function
function highlightMap(hives, pointClass, pointFunction) {
    let circles = d3.selectAll("circle.cities")
    clearMarks(d3.selectAll(`circle.${pointClass}`), pointClass)
    circles.each((d, i, elements) => {
        if(hives.includes(d['Hive ID'])) {
            pointFunction(elements[i],pointClass)
        }
    })
}

function containsPlantHighlightMap(hives, pointClass, pointFunction) {
    let circles = d3.selectAll("circle.cities")
    clearMarks(d3.selectAll(`circle.${pointClass}`), pointClass)
    circles.each((d, i, elements) => {
        if(!hives.includes(d['Hive ID'])) {
            pointFunction(elements[i],pointClass)
        }
    })
}

//Grows a selected point and assigns the given class to a point 
function markPoint (element, pointClass) {
    let currentElement = d3.select(element).raise();
    currentElement
        .classed(pointClass, true)
        .transition()
        .duration(100)
        .attr('r', 20);
}

//Assigns a class to a point
function hidePoint (element, pointClass) {
    let currentElement = d3.select(element);
    currentElement.classed(pointClass, true)
}

//Removes the given class and returns the point to normal
function clearMarks(elements, pointClass) {
    elements.each((d, i, elements) => {
    d3.select(elements[i])
    .classed(pointClass, false)
    .transition()
    .duration(100)
    .attr('r', 4)
    })
}

//Highlights all hives provided with containsPlant class.
function listContainsPlant(hiveList) {
    d3.selectAll('.noPlant').classed("noPlant", false)
    d3.selectAll('.containsPlant').classed("containsPlant", false)
    containsPlantHighlightMap(hiveList, "noPlant", hidePoint)
    d3.selectAll('circle:not(.noPlant)').raise()
    d3.selectAll(".selected").raise()
    let row = d3.selectAll('tr')
    .each((d, i, elements) => {
        if(d == null || hiveList == null) {
            return
        } else if (hiveList.includes(d['Hive ID'])){
            d3.select(elements[i]).classed("containsPlant", true);
        }
    });
}