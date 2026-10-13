const form = document.getElementById('car-form');
const carId = document.getElementById('car-id');
const tbody = document.getElementById('cars-tbody');
const messageEl = document.getElementById('message');
const submitBtn = document.getElementById('submit-btn');
const resetBtn = document.getElementById('reset-btn');

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const detail = (await res.json().catch(() => ({}))).detail || res.statusText;
    throw new Error(detail);
  }
  return res.status === 204 ? null : res.json();
}

function showMessage(text, error = false) {
  messageEl.textContent = text;
  messageEl.hidden = false;
  messageEl.style.background = error ? '#fef2f2' : '#ecfdf3';
  messageEl.style.color = error ? '#b91c1c' : '#067647';
  setTimeout(() => { messageEl.hidden = true; }, 3000);
}

async function loadCars() {
  const cars = await api('/api/cars');
  tbody.innerHTML = '';
  for (const car of cars) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${car.id}</td>
      <td>${car.make}</td>
      <td>${car.model}</td>
      <td>${car.year ?? ''}</td>
      <td>${car.color ?? ''}</td>
      <td class="actions">
        <a data-act="edit" data-id="${car.id}">Edit</a>
        <a class="delete" data-act="delete" data-id="${car.id}">Delete</a>
      </td>`;
    tbody.appendChild(row);
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    make: document.getElementById('make').value.trim(),
    model: document.getElementById('model').value.trim(),
    year: document.getElementById('year').value ? Number(document.getElementById('year').value) : null,
    color: document.getElementById('color').value.trim() || null,
  };
  try {
    const id = carId.value;
    if (id) {
      await api(`/api/cars/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
      showMessage('Car updated');
    } else {
      await api('/api/cars', { method: 'POST', body: JSON.stringify(payload) });
      showMessage('Car added');
    }
    form.reset();
    carId.value = '';
    resetBtn.hidden = true;
    submitBtn.textContent = 'Add car';
    await loadCars();
  } catch (err) {
    showMessage(err.message, true);
  }
});

tbody.addEventListener('click', async (e) => {
  const link = e.target.closest('a[data-act]');
  if (!link) return;
  const id = link.dataset.id;
  if (link.dataset.act === 'delete') {
    try {
      await api(`/api/cars/${id}`, { method: 'DELETE' });
      showMessage('Car deleted');
      await loadCars();
    } catch (err) { showMessage(err.message, true); }
    return;
  }
  // edit: prefill the form
  const cars = await api('/api/cars');
  const car = cars.find((c) => String(c.id) === id);
  carId.value = car.id;
  document.getElementById('make').value = car.make;
  document.getElementById('model').value = car.model;
  document.getElementById('year').value = car.year ?? '';
  document.getElementById('color').value = car.color ?? '';
  resetBtn.hidden = false;
  submitBtn.textContent = 'Save changes';
});

resetBtn.addEventListener('click', () => {
  form.reset();
  carId.value = '';
  resetBtn.hidden = true;
  submitBtn.textContent = 'Add car';
});

loadCars();
