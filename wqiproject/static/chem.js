// -------------------- WQI CALCULATION SCRIPT ---------------------

// BIS / WHO Standard values for drinking water
const standards = {
    pH: 7.0,             // ideal
    pH_max: 8.5,         // permissible limit
    TDS: 500,            // mg/L
    Hardness: 300,       // mg/L
    Turbidity: 5,        // NTU
    Conductivity: 1500   // µS/cm (optional)
};

// Assigning weights (importance of each parameter)
const weights = {
    pH: 0.22,
    TDS: 0.28,
    Hardness: 0.20,
    Turbidity: 0.20,
    Conductivity: 0.10
};

// Function to compute quality rating (Qi)
function computeQi(measured, ideal, standardLimit) {
    return ((measured - ideal) / (standardLimit - ideal)) * 100;
}

// Function to compute WQI
function calculateWQI() {

    // Fetch user inputs
    const ph = parseFloat(document.getElementById("ph").value);
    const tds = parseFloat(document.getElementById("tds").value);
    const hardness = parseFloat(document.getElementById("hardness").value);
    const turbidity = parseFloat(document.getElementById("turbidity").value);
    const conductivity = parseFloat(document.getElementById("Conductivity").value);

    if (!ph || !tds || !hardness || !turbidity) {
        alert("⚠️ Please fill all mandatory fields (Conductivity optional).");
        return;
    }
    if(ph>=14 && ph<0){
        alert("ph out of rangee !")
        return;
    }
    let qi = {};
    let wiQi = 0;
    let sumWi = 0;

    // pH
    qi.pH = computeQi(ph, standards.pH, standards.pH_max);
    wiQi += qi.pH * weights.pH;
    sumWi += weights.pH;

    // TDS
    qi.TDS = computeQi(tds, 0, standards.TDS);
    wiQi += qi.TDS * weights.TDS;
    sumWi += weights.TDS;

    // Hardness
    qi.Hardness = computeQi(hardness, 0, standards.Hardness);
    wiQi += qi.Hardness * weights.Hardness;
    sumWi += weights.Hardness;

    // Turbidity
    qi.Turbidity = computeQi(turbidity, 0, standards.Turbidity);
    wiQi += qi.Turbidity * weights.Turbidity;
    sumWi += weights.Turbidity;

    // Conductivity (optional)
    if (!isNaN(conductivity) && conductivity > 0) {
        qi.Conductivity = computeQi(conductivity, 0, standards.Conductivity);
        wiQi += qi.Conductivity * weights.Conductivity;
        sumWi += weights.Conductivity;
    }

    // Final Water Quality Index
    const WQI = (wiQi / sumWi).toFixed(2);

    displayResult(WQI);
}

//updating display

// let btn=document.querySelector(".form");
// btn.addEventListener("submit",function(){
//  document.getElementById("WQI").textContent=calculateWQI()
// })
   
// Display the WQI result with quality meaning
function displayResult(WQI) {
    let quality = "Unsuitable for Drinking ⚠️";
    if (WQI <= 50 && WQI>=0) quality = "Excellent 💧";
    else if(WQI<0) quaality=""
    else if (WQI <= 100) quality = "Good 🙂";
    else if (WQI <= 200) quality = "Poor 😕";
    else if (WQI <= 300) quality = "Very Poor 😣";
    else quality = "Unsuitable for Drinking ⚠️";

    document.getElementById("result").innerHTML =
        `WQI = <strong>${WQI}</strong> → <strong>${quality}</strong>`;
}

// Attach event listener to button
let main=document.querySelector(".main");
let good=document.querySelector(".good");
let back=document.querySelector(".back");
document.querySelector(".check").addEventListener("click", function(e){
    e.preventDefault();
    main.classList.add("none");
    good.classList.remove("none");
    calculateWQI();
    
});
back.addEventListener("click",(e)=>{
     e.preventDefault();
       main.classList.remove("none");
    good.classList.add("none");
})

