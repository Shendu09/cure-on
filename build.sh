#!/bin/bash

# Render build script - runs during deployment

echo "🔨 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Download sentence-transformers model ahead of time
echo "📥 Pre-downloading embedding model..."
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/raw
mkdir -p data/vector_store

# Create sample data if no data exists
echo "📝 Setting up sample medical data..."
python -c "
import json
from pathlib import Path

data_dir = Path('data/raw')

# Sample medical documents
samples = [
    {
        'filename': 'diabetes_info.txt',
        'content': '''Diabetes Mellitus Overview

Type 1 Diabetes:
- Autoimmune condition where the pancreas produces little or no insulin
- Usually diagnosed in children and young adults
- Requires daily insulin injections
- Symptoms: increased thirst, frequent urination, extreme hunger, weight loss

Type 2 Diabetes:
- Most common form (90-95% of cases)
- Body becomes resistant to insulin or doesn't produce enough
- Risk factors: obesity, physical inactivity, family history, age over 45
- Symptoms: similar to Type 1 but develop more gradually
- Management: lifestyle changes, oral medications, sometimes insulin

Prevention and Management:
- Maintain healthy weight
- Regular physical activity (150 minutes per week)
- Balanced diet rich in vegetables, whole grains, lean proteins
- Regular blood sugar monitoring
- Annual eye and foot examinations
'''
    },
    {
        'filename': 'hypertension_guide.txt',
        'content': '''Hypertension (High Blood Pressure) Guide

What is Hypertension?
Blood pressure consistently above 130/80 mmHg

Categories:
- Normal: Less than 120/80 mmHg
- Elevated: 120-129/<80 mmHg
- Stage 1: 130-139/80-89 mmHg
- Stage 2: 140+/90+ mmHg
- Crisis: 180+/120+ mmHg (seek immediate care)

Risk Factors:
- Age (risk increases with age)
- Family history
- Obesity
- High sodium intake
- Lack of physical activity
- Tobacco use
- Excessive alcohol consumption
- Chronic stress

Treatment Options:
1. Lifestyle Modifications:
   - DASH diet (Dietary Approaches to Stop Hypertension)
   - Reduce sodium to <2300mg/day
   - Regular aerobic exercise
   - Limit alcohol
   - Stress management
   - Maintain healthy weight

2. Medications (if needed):
   - ACE inhibitors
   - ARBs (Angiotensin II receptor blockers)
   - Calcium channel blockers
   - Diuretics
   - Beta-blockers

Monitoring:
- Home blood pressure monitoring
- Regular check-ups with healthcare provider
- Target: <130/80 mmHg for most adults
'''
    },
    {
        'filename': 'common_cold_vs_flu.json',
        'content': {
            'title': 'Common Cold vs Influenza (Flu)',
            'common_cold': {
                'onset': 'Gradual over several days',
                'fever': 'Rare in adults, sometimes in children',
                'symptoms': [
                    'Runny or stuffy nose',
                    'Sore throat',
                    'Sneezing',
                    'Mild cough',
                    'Mild body aches'
                ],
                'duration': '7-10 days',
                'complications': 'Rare (sinus infection, ear infection)',
                'treatment': [
                    'Rest and fluids',
                    'Over-the-counter cold medications',
                    'Throat lozenges',
                    'Saline nasal drops',
                    'Humidifier use'
                ]
            },
            'influenza': {
                'onset': 'Sudden, within hours',
                'fever': 'Common, often 100-104°F (38-40°C)',
                'symptoms': [
                    'High fever',
                    'Severe body aches',
                    'Extreme fatigue',
                    'Dry cough',
                    'Headache',
                    'Sometimes sore throat and stuffy nose'
                ],
                'duration': '1-2 weeks',
                'complications': 'Can be serious (pneumonia, bronchitis, sinus infections)',
                'treatment': [
                    'Antiviral medications (if started within 48 hours)',
                    'Rest and fluids',
                    'Fever reducers',
                    'Pain relievers',
                    'Medical attention if symptoms worsen'
                ],
                'prevention': [
                    'Annual flu vaccine',
                    'Frequent handwashing',
                    'Avoid close contact with sick people',
                    'Cover coughs and sneezes'
                ]
            },
            'when_to_see_doctor': [
                'Difficulty breathing or shortness of breath',
                'Chest pain or pressure',
                'Sudden dizziness or confusion',
                'Severe or persistent vomiting',
                'Symptoms that improve but then return with fever and worse cough',
                'Fever above 103°F (39.4°C)'
            ]
        }
    }
]

for sample in samples:
    filepath = data_dir / sample['filename']
    if sample['filename'].endswith('.json'):
        with open(filepath, 'w') as f:
            json.dump(sample['content'], f, indent=2)
    else:
        with open(filepath, 'w') as f:
            f.write(sample['content'])

print(f'✓ Created {len(samples)} sample medical documents')
"

echo "✅ Build complete!"
