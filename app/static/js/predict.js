const RANGES = {
    temperature: { min: 90, max: 140, label: 'Temperature' },
    moisture: { min: 0, max: 10, label: 'Moisture' },
    ph: { min: 2, max: 9, label: 'pH' },
    color_score: { min: 0, max: 100, label: 'Color Score' },
    cooking_time: { min: 30, max: 150, label: 'Cooking Time' },
    dryness_level: { min: 1, max: 5, label: 'Dryness Level' },
};

const ALLOWED_SUPPLIERS = ['Central Java', 'Central Kalimantan', 'East Java', 'West Java', 'Yogyakarta'];

function validateForm() {
    for (const [field, range] of Object.entries(RANGES)) {
        const el = document.getElementById(field);
        const val = parseFloat(el.value);
        if (isNaN(val) || val < range.min || val > range.max) {
            return { valid: false, error: `${range.label} must be between ${range.min} and ${range.max}` };
        }
    }

    const supplier = document.getElementById('supplier_origin').value;
    if (!ALLOWED_SUPPLIERS.includes(supplier)) {
        return { valid: false, error: 'Please select a valid supplier' };
    }

    const visual = document.getElementById('visual_inspection').value;
    if (!['poor', 'fair', 'good', 'excellent'].includes(visual)) {
        return { valid: false, error: 'Please select a valid visual inspection result' };
    }

    return { valid: true };
}

function showError(message) {
    const errEl = document.getElementById('form-error');
    errEl.textContent = message;
    errEl.style.display = 'block';
    setTimeout(() => { errEl.style.display = 'none'; }, 5000);
}

function displayResult(data) {
    const card = document.getElementById('result-card');
    card.style.display = 'block';

    const gradeEl = document.getElementById('result-grade');
    gradeEl.textContent = data.grade;

    const colors = {
        'Grade A': 'var(--success)',
        'Grade B': 'var(--warning)',
        'Reject': 'var(--danger)',
    };
    gradeEl.style.color = colors[data.grade] || 'var(--text)';

    document.getElementById('result-confidence').textContent = (data.confidence * 100).toFixed(1);
    document.getElementById('result-recommendation').textContent = data.recommendation;
}

document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const resultCard = document.getElementById('result-card');
    resultCard.style.display = 'none';
    const errorEl = document.getElementById('form-error');
    errorEl.style.display = 'none';

    const validation = validateForm();
    if (!validation.valid) {
        showError(validation.error);
        return;
    }

    const btn = document.getElementById('submit-btn');
    btn.disabled = true;
    btn.textContent = 'Predicting...';

    const payload = {
        temperature: parseFloat(document.getElementById('temperature').value),
        moisture: parseFloat(document.getElementById('moisture').value),
        pH: parseFloat(document.getElementById('ph').value),
        color_score: parseFloat(document.getElementById('color_score').value),
        cooking_time: parseInt(document.getElementById('cooking_time').value),
        dryness_level: parseInt(document.getElementById('dryness_level').value),
        supplier_origin: document.getElementById('supplier_origin').value,
        visual_inspection: document.getElementById('visual_inspection').value,
    };

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await res.json();

        if (res.ok) {
            displayResult(data);
        } else {
            showError(data.error || 'Prediction failed');
        }
    } catch (err) {
        showError('Network error: ' + err.message);
    }

    btn.disabled = false;
    btn.textContent = 'Get Prediction';
});
