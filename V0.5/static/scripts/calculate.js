// Source: https://onecompiler.com/html/3zpx74xq4
document.addEventListener("DOMContentLoaded", function () {
    const calculateButton = document.getElementById("calculate");
    const distanceInput = document.getElementById("distance");
    const emissionInput = document.getElementById("emission");
    const carbonScore = document.getElementById("carbon-score");

    calculateButton.addEventListener("click", function () {
        const distance = parseFloat(distanceInput.value);
        const emissionFactor = parseFloat(emissionInput.value);

        if (!isNaN(distance) && !isNaN(emissionFactor)) {
            const carbon = distance * emissionFactor;
            carbonScore.textContent = "Carbon Score: " + carbon.toFixed(2) + " CO2e";
        } else {
            carbonScore.textContent = "Carbon Score: Invalid Input";
        }
    });
});


