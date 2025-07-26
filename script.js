document.getElementById("location-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const lat = document.getElementById("lat").value;
  const lon = document.getElementById("lon").value;

  const selectedAllergies = Array.from(
    document.querySelectorAll("input[name='allergy']:checked")
  ).map((el) => el.value);

  const response = await fetch("/pollen", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ lat, lon, selectedAllergies }),
  });

  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML = ""; // clear previous results

  if (!response.ok) {
    const errorData = await response.json();
    resultDiv.innerHTML = `<div class="error-box">❌ ${errorData.error}</div>`;
    return;
  }

  const data = await response.json();

  const dateEl = document.createElement("h2");
  dateEl.textContent = `📅 Pollen Report for ${data.data}`;
  resultDiv.appendChild(dateEl);

  data.pollen.forEach((pollen) => {
    const card = document.createElement("div");
    card.className = "pollen-card";

    // Set color class
    if (pollen.value <= 2) {
      card.classList.add("green");
    } else if (pollen.value === 3) {
      card.classList.add("yellow");
    } else {
      card.classList.add("red");
    }

    card.innerHTML = `
      <h3>${pollen.name} 🌿</h3>
      <p><strong>Level:</strong> ${pollen.value} (${pollen.category})</p>
      <p>${pollen.description}</p>
    `;
    resultDiv.appendChild(card);
  });
});