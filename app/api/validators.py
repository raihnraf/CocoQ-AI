ALLOWED_SUPPLIERS = {
    'Central Java', 'Central Kalimantan', 'East Java', 'West Java', 'Yogyakarta',
}
ALLOWED_VISUAL = {'poor', 'fair', 'good', 'excellent'}

REQUIRED_FIELDS = [
    'temperature', 'moisture', 'pH', 'color_score', 'cooking_time',
    'supplier_origin', 'dryness_level', 'visual_inspection',
]

RANGES = {
    'temperature': (90, 140),
    'moisture': (0, 10),
    'pH': (2, 9),
    'color_score': (0, 100),
    'cooking_time': (30, 150),
    'dryness_level': (1, 5),
}


def validate_batch_input(data):
    if data is None:
        return None, 'Request body must be valid JSON'

    for field in REQUIRED_FIELDS:
        if field not in data:
            return None, f'Missing required field: {field}'

    cleaned = {}

    numeric_fields = ['temperature', 'moisture', 'pH', 'color_score', 'cooking_time']
    for field in numeric_fields:
        try:
            cleaned[field] = float(data[field])
        except (ValueError, TypeError):
            return None, f'Invalid value for {field}: must be a number'

        low, high = RANGES[field]
        if cleaned[field] < low or cleaned[field] > high:
            return None, f'Invalid value for {field}: must be between {low} and {high}'

    try:
        cleaned['dryness_level'] = int(data['dryness_level'])
    except (ValueError, TypeError):
        return None, 'Invalid value for dryness_level: must be an integer'

    low, high = RANGES['dryness_level']
    if cleaned['dryness_level'] < low or cleaned['dryness_level'] > high:
        return None, f'Invalid value for dryness_level: must be between {low} and {high}'

    supplier = str(data['supplier_origin']).strip().title()
    if supplier not in ALLOWED_SUPPLIERS:
        return None, f"Invalid supplier_origin: must be one of {sorted(ALLOWED_SUPPLIERS)}"
    cleaned['supplier_origin'] = supplier

    visual = str(data['visual_inspection']).strip().lower()
    if visual not in ALLOWED_VISUAL:
        return None, f"Invalid visual_inspection: must be one of {sorted(ALLOWED_VISUAL)}"
    cleaned['visual_inspection'] = visual

    return cleaned, None
