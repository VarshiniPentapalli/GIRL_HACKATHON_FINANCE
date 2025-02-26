GEMINI_API_KEY = 'AIzaSyC2f8KVSvnGGC0lkfi7WufOLVVAwvVxkdE'  # Replace with your actual API key

TAX_RULES = {
    'USA': {
        'standard_deduction': 12550,
        'tax_brackets': [
            (0, 9950, 0.10),
            (9951, 40525, 0.12),
            (40526, 86375, 0.22),
            # Add more brackets as needed
        ]
    },
    'India': {
        'standard_deduction': 50000,
        'tax_brackets': [
            (0, 250000, 0),
            (250001, 500000, 0.05),
            (500001, 750000, 0.10),
            # Add more brackets as needed
        ]
    }
}
