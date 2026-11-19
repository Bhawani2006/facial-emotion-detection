"""
Creates a professional Word document with the complete emotion detection system prompt
for use in Google AI Studio or other AI development tools.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_hyperlink(paragraph, url, text):
    """Add a hyperlink to a paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    
    paragraph._p.append(hyperlink)
    
    run = paragraph.runs[-1]
    run.font.color.rgb = RGBColor(0, 0, 255)
    run.font.underline = True
    return hyperlink

def create_emotion_detection_doc():
    """Create comprehensive Word document for emotion detection system."""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════════════════════════
    
    title = doc.add_heading('Real-Time Multi-Face Emotion Detection System', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_heading('Complete Development Guide for Google AI Studio', level=2)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('Production-Ready AI System\n').bold = True
    info.add_run('With Multi-Face Tracking, Gender Detection, Glasses Classification\n')
    info.add_run('30 FPS Real-Time Performance | Apple-Inspired UI\n')
    
    doc.add_page_break()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('Table of Contents', level=1)
    
    toc_items = [
        ('1', 'Project Overview'),
        ('2', 'Technical Requirements'),
        ('3', 'Architecture Components'),
        ('  3.1', 'Emotion Detection Model (Deep CNN)'),
        ('  3.2', 'Gender Detection Model (Binary CNN)'),
        ('  3.3', 'Glasses Detection System'),
        ('  3.4', 'Real-Time Processing Pipeline'),
        ('  3.5', 'User Interface Design'),
        ('  3.6', 'Voice Feedback System'),
        ('4', 'Step-by-Step Implementation Guide'),
        ('  4.1', 'Phase 1: Environment Setup'),
        ('  4.2', 'Phase 2: Emotion Model Training'),
        ('  4.3', 'Phase 3: Gender Model Training'),
        ('  4.4', 'Phase 4: Real-Time Detector Implementation'),
        ('  4.5', 'Phase 5: Testing & Validation'),
        ('5', 'Dataset Acquisition'),
        ('6', 'Performance Optimization Tips'),
        ('7', 'Troubleshooting Guide'),
        ('8', 'Advanced Features'),
        ('9', 'References & Resources'),
    ]
    
    for num, item in toc_items:
        p = doc.add_paragraph(style='List Number' if not num.startswith('  ') else 'List Bullet')
        p.add_run(f'{num}. {item}')
    
    doc.add_page_break()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 1. PROJECT OVERVIEW
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('1. Project Overview', level=1)
    
    doc.add_paragraph(
        'Build a production-ready real-time facial emotion detection application with '
        'advanced features including multi-face tracking, gender classification, and '
        'eyewear detection. This system achieves 30 FPS performance with modern UI design.'
    )
    
    doc.add_heading('Core Features', level=2)
    
    features = [
        '5 Emotion Classes: Angry, Fear, Happy, Sad, Neutral',
        'Multi-Face Tracking: Detect and track 9-10 faces simultaneously',
        '30 FPS Performance: Real-time processing at locked 30 frames per second',
        'Gender Detection: Male/Female classification with 95%+ accuracy',
        'Glasses Detection: Distinguish between eyeglasses and sunglasses',
        'Adaptive Lighting: Auto-enhance for dark rooms and low-light conditions',
        'Modern UI: Apple-inspired sleek interface with dark/light themes',
        'Voice Feedback: Non-blocking Text-to-Speech for behavioral alerts',
    ]
    
    for feature in features:
        doc.add_paragraph(feature, style='List Bullet')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 2. TECHNICAL REQUIREMENTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('2. Technical Requirements', level=1)
    
    doc.add_heading('Core Technologies', level=2)
    
    tech = [
        ('Python', '3.8 or higher'),
        ('TensorFlow', '2.12 or higher (Deep Learning framework)'),
        ('OpenCV', '4.8 or higher (Computer vision and camera interface)'),
        ('NumPy', '1.23 or higher (Numerical operations)'),
        ('Matplotlib', '3.7 or higher (Training visualization)'),
        ('scikit-learn', '1.2 or higher (Metrics and evaluation)'),
        ('Windows SAPI5', 'Built-in (Text-to-speech voice feedback)'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Technology'
    hdr_cells[1].text = 'Version / Details'
    
    for name, version in tech:
        row_cells = table.add_row().cells
        row_cells[0].text = name
        row_cells[1].text = version
    
    doc.add_paragraph()
    
    doc.add_heading('Hardware Requirements', level=2)
    
    hw = [
        'Webcam: 720p or 1080p (30 FPS capable)',
        'CPU: Multi-core processor (Intel i5+ or AMD Ryzen 5+)',
        'RAM: 8GB minimum, 16GB recommended',
        'OS: Windows 10/11 (for SAPI5 voice synthesis)',
        'Disk Space: 2GB for datasets, 50MB for models',
    ]
    
    for item in hw:
        doc.add_paragraph(item, style='List Bullet')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 3. ARCHITECTURE COMPONENTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('3. Architecture Components', level=1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3.1 Emotion Detection Model
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('3.1 Emotion Detection Model (Deep CNN)', level=2)
    
    doc.add_paragraph(
        'The emotion detection system uses a deep convolutional neural network (CNN) '
        'trained to classify facial expressions into 5 categories.'
    )
    
    doc.add_heading('Model Architecture', level=3)
    
    doc.add_paragraph('Input: 48×48 grayscale face images').bold = True
    doc.add_paragraph()
    
    arch_text = """
Block 1 - Basic Edge Features:
• Conv2D(64, 3×3) + BatchNorm + ReLU
• Conv2D(64, 3×3) + BatchNorm + ReLU
• MaxPooling2D(2×2)
• Dropout(0.25)

Block 2 - Facial Region Features:
• Conv2D(128, 3×3) + BatchNorm + ReLU
• Conv2D(128, 3×3) + BatchNorm + ReLU
• MaxPooling2D(2×2)
• Dropout(0.25)

Block 3 - Action Unit Features (eyebrows, mouth):
• Conv2D(256, 3×3) + BatchNorm + ReLU
• Conv2D(256, 3×3) + BatchNorm + ReLU
• MaxPooling2D(2×2)
• Dropout(0.30)

Block 4 - Abstract Discriminative Features:
• Conv2D(512, 3×3) + BatchNorm + ReLU
• GlobalAveragePooling2D()

Classifier Head:
• Dense(256) + BatchNorm + ReLU
• Dropout(0.50)
• Dense(5, activation='softmax') → Output: [Angry, Fear, Happy, Sad, Neutral]
"""
    
    doc.add_paragraph(arch_text)
    
    doc.add_heading('Training Configuration', level=3)
    
    train_config = [
        ('Dataset', 'FER-2013 or similar (17,627+ training images)'),
        ('Image Size', '48×48 grayscale'),
        ('Batch Size', '64'),
        ('Epochs', '60 with early stopping (patience=15)'),
        ('Learning Rate', '5e-4 with cosine decay'),
        ('Label Smoothing', '0.1 (prevents overconfident predictions)'),
        ('Loss Function', 'Categorical crossentropy'),
        ('Optimizer', 'Adam'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light List Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Parameter'
    hdr_cells[1].text = 'Value'
    
    for param, value in train_config:
        row_cells = table.add_row().cells
        row_cells[0].text = param
        row_cells[1].text = value
    
    doc.add_paragraph()
    
    doc.add_heading('Data Augmentation Strategy', level=3)
    
    aug = [
        'Rotation: ±20 degrees',
        'Width/Height Shift: ±18%',
        'Shear Transformation: ±12%',
        'Zoom Range: ±18%',
        'Horizontal Flip: Enabled',
        'Brightness Range: 70-130% (Critical for webcam generalization)',
    ]
    
    for item in aug:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('Critical Training Fixes', level=3)
    
    p = doc.add_paragraph()
    p.add_run('IMPORTANT: ').bold = True
    p.add_run('These fixes are essential for production-quality results:')
    
    fixes = [
        'Use label smoothing (0.1) to prevent overconfident softmax outputs',
        'Use larger dataset (17K+ images, NOT 5K)',
        'Implement cosine learning rate decay with 5-epoch warmup',
        'Train for full 60 epochs instead of premature early stopping',
        'Apply strong brightness augmentation (70-130%) for webcam robustness',
        'Balanced class weights with mild boosts (not 2× distortion)',
    ]
    
    for fix in fixes:
        doc.add_paragraph(fix, style='List Number')
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3.2 Gender Detection Model
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('3.2 Gender Detection Model (Binary CNN)', level=2)
    
    doc.add_paragraph(
        'Binary classification system for Male/Female detection. Achieves 92-95% accuracy '
        'when trained on real labeled data (UTKFace dataset).'
    )
    
    doc.add_heading('Model Architecture', level=3)
    
    gender_arch = """
Input: 64×64 grayscale face images

Block 1:
• Conv2D(32, 3×3) + BatchNorm + ReLU
• MaxPooling2D(2×2)
• Dropout(0.25)

Block 2:
• Conv2D(64, 3×3) + BatchNorm + ReLU
• MaxPooling2D(2×2)
• Dropout(0.25)

Block 3:
• Conv2D(128, 3×3) + BatchNorm + ReLU
• MaxPooling2D(2×2)
• Dropout(0.25)

Classifier:
• Flatten()
• Dense(256) + BatchNorm + ReLU
• Dropout(0.50)
• Dense(1, activation='sigmoid') → Output: 0=Male, 1=Female
"""
    
    doc.add_paragraph(gender_arch)
    
    doc.add_heading('CRITICAL: Dataset Requirement', level=3)
    
    p = doc.add_paragraph()
    p.add_run('⚠ WARNING: ').bold = True
    p.add_run('Gender model MUST be trained on UTKFace dataset with real labels. '
              'Training on emotion datasets with pseudo-labels results in only 60-70% accuracy.')
    
    doc.add_paragraph()
    
    dataset_info = [
        ('Dataset Name', 'UTKFace'),
        ('Source', 'Kaggle: nipunarora8/utkface-new'),
        ('Size', '24,000+ diverse face images'),
        ('Age Range', '0-116 years'),
        ('Ethnicities', 'Multiple (White, Black, Asian, Indian, Other)'),
        ('Labels', 'Real ground-truth gender labels (NOT pseudo-labels)'),
        ('Filename Format', 'age_gender_race_date.jpg (gender: 0=Male, 1=Female)'),
        ('Expected Accuracy', '92-95% validation, 90-93% webcam'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Property'
    hdr_cells[1].text = 'Details'
    
    for prop, detail in dataset_info:
        row_cells = table.add_row().cells
        row_cells[0].text = prop
        row_cells[1].text = detail
    
    doc.add_paragraph()
    
    doc.add_heading('Temporal Smoothing', level=3)
    
    doc.add_paragraph(
        'To prevent jittery label switching between frames, the system uses Exponential '
        'Moving Average (EMA) with alpha=0.40 per face ID. This maintains stable gender '
        'predictions across frames.'
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3.3 Glasses Detection
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('3.3 Glasses Detection System', level=2)
    
    doc.add_paragraph(
        'Hybrid detection system combining Haar cascades and brightness analysis to '
        'distinguish between eyeglasses, sunglasses, and no glasses.'
    )
    
    doc.add_heading('Detection Components', level=3)
    
    components = [
        'Haar Cascade: haarcascade_eye_tree_eyeglasses.xml (glasses-aware)',
        'Haar Cascade: haarcascade_eye.xml (bare eyes)',
        'Brightness Analysis: Mean pixel value < 45 → likely sunglasses',
        'Edge Density: Canny edge detection, fraction > 0.06 → eyeglasses frame',
    ]
    
    for comp in components:
        doc.add_paragraph(comp, style='List Bullet')
    
    doc.add_heading('Classification Logic', level=3)
    
    logic = """
IF glasses_cascade detects AND eye_cascade does NOT:
    → eyeglasses (confidence 0.70 + edge_fraction × 8)

ELSE IF both cascades fail AND brightness < 45:
    → sunglasses (confidence 0.85 if std < 30, else 0.65)

ELSE IF eye_cascade detects:
    → none (confidence 0.80)

ELSE IF edge_fraction > 0.09:
    → eyeglasses (confidence 0.60)

ELSE:
    → none
"""
    
    doc.add_paragraph(logic)
    
    doc.add_heading('Temporal Smoothing', level=3)
    doc.add_paragraph('Window size: 8 frames with majority voting for stable classification.')
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3.4 Real-Time Processing Pipeline
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('3.4 Real-Time Processing Pipeline', level=2)
    
    doc.add_paragraph(
        'Multi-threaded architecture optimized for 30 FPS performance with multiple faces.'
    )
    
    doc.add_heading('Performance Optimizations', level=3)
    
    opt_table = [
        ('Multi-Threaded Webcam', 'Dedicated capture thread with DirectShow backend, MJPEG compression, buffer=1'),
        ('Async Inference', 'Separate thread for CNN predictions with non-blocking queue'),
        ('Face Detection Skip', 'Run every 2 frames (30→15 FPS detection) with temporal tracking'),
        ('Face Margin', '2% expansion (matches tight FER-2013 training crops)'),
        ('Batch Processing', 'Process multiple faces in single batch when available'),
        ('Temperature Scaling', 'Sharpen predictions with T=0.85 for confidence'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Medium Grid 1 Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Optimization'
    hdr_cells[1].text = 'Implementation'
    
    for opt, impl in opt_table:
        row_cells = table.add_row().cells
        row_cells[0].text = opt
        row_cells[1].text = impl
    
    doc.add_paragraph()
    
    doc.add_heading('Adaptive Lighting (Dark Room Mode)', level=3)
    
    lighting = """
def auto_light(gray_image):
    mean_brightness = np.mean(gray_image)
    
    if mean_brightness < 60:  # Dark room detected
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8,8))
        enhanced = clahe.apply(gray_image)
        
        if mean_brightness < 40:  # Very dark
            # Apply gamma correction (gamma=1.65)
            enhanced = cv2.LUT(enhanced, GAMMA_LUT)
        
        return enhanced, True  # is_low_light
    
    return gray_image, False
"""
    
    doc.add_paragraph(lighting, style='No Spacing')
    
    doc.add_heading('Smile Correction System', level=3)
    
    p = doc.add_paragraph()
    p.add_run('CRITICAL: ').bold = True
    p.add_run('Apply smile correction ONCE per prediction to prevent Happy→Sad misclassification.')
    
    doc.add_paragraph()
    
    smile = """
def apply_smile_correction(emotion_probs, smile_score):
    if smile_score < 0.18:
        return emotion_probs  # No correction needed
    
    corrected = emotion_probs.copy()
    corrected[0] *= 1.0 - 0.08 * smile_score  # Angry ↓ (gentle)
    corrected[1] *= 1.0 - 0.05 * smile_score  # Fear ↓
    corrected[2] *= 1.0 + 0.15 * smile_score  # Happy ↑
    corrected[3] *= 1.0 - 0.08 * smile_score  # Sad ↓
    
    return corrected / corrected.sum()  # Renormalize
"""
    
    doc.add_paragraph(smile, style='No Spacing')
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3.5 User Interface
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('3.5 User Interface (Apple-Inspired Design)', level=2)
    
    doc.add_paragraph(
        'Modern, sleek interface inspired by Apple design language with dark/light themes, '
        'translucent cards, and rounded corners.'
    )
    
    doc.add_heading('Visual Components', level=3)
    
    ui_components = [
        ('Top Navigation Bar', '50px height, shows title, FPS, resolution, voice status, theme, sharp mode'),
        ('Face Bounding Boxes', 'Corner brackets style (minimal), color-coded by emotion, 2px thickness'),
        ('Emotion Badge', 'Floating pill card above face: "Person #N - Emotion XX%"'),
        ('Gender & Glasses Badge', 'Below face: "[M] Male 85% | Eyeglasses 78%"'),
        ('Side Panel Statistics', 'Per-emotion confidence bars (280px width, pill-shaped progress bars)'),
        ('Bottom Control Bar', 'Keyboard shortcuts: Q=Quit, E=Quality, T=Theme, V=Voice'),
    ]
    
    for comp, desc in ui_components:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f'{comp}: ').bold = True
        p.add_run(desc)
    
    doc.add_heading('Emotion Color Palette', level=3)
    
    colors = [
        ('Angry', 'Red', 'RGB(255, 59, 48)'),
        ('Fear', 'Purple', 'RGB(88, 86, 214)'),
        ('Happy', 'Green', 'RGB(52, 199, 89)'),
        ('Sad', 'Blue', 'RGB(0, 113, 227)'),
        ('Neutral', 'Gray', 'RGB(161, 161, 166)'),
    ]
    
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Colorful List Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Emotion'
    hdr_cells[1].text = 'Color'
    hdr_cells[2].text = 'RGB Value'
    
    for emotion, color, rgb in colors:
        row_cells = table.add_row().cells
        row_cells[0].text = emotion
        row_cells[1].text = color
        row_cells[2].text = rgb
    
    doc.add_paragraph()
    
    doc.add_heading('Theme Palettes', level=3)
    
    themes = [
        ('Dark Theme', 'bg_card=(18,18,22), txt_primary=(245,245,247), bar_track=(38,38,44)'),
        ('Light Theme', 'bg_card=(252,252,254), txt_primary=(29,29,31), bar_track=(230,232,238)'),
    ]
    
    for theme, values in themes:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f'{theme}: ').bold = True
        p.add_run(values)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3.6 Voice Feedback
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('3.6 Voice Feedback System', level=2)
    
    doc.add_paragraph(
        'Non-blocking Text-to-Speech engine for behavioral alerts with intelligent cooldown.'
    )
    
    voice_features = [
        'Background thread with message queue',
        'Windows SAPI5 (win32com.client) as primary TTS engine',
        'PowerShell System.Speech as automatic fallback',
        'Cooldown: 4 seconds between messages',
        'Duplicate message prevention',
        'Toggle on/off with "V" key',
    ]
    
    for feature in voice_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('Voice Triggers', level=3)
    
    triggers = [
        'Sustained negative emotions (Angry/Sad > 5 seconds)',
        'Frustration patterns detected',
        'Fatigue behavioral alerts',
        'Example: "You seem stressed. Consider taking a break."',
    ]
    
    for trigger in triggers:
        doc.add_paragraph(trigger, style='List Bullet')
    
    doc.add_page_break()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 4. STEP-BY-STEP IMPLEMENTATION GUIDE
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('4. Step-by-Step Implementation Guide', level=1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Phase 1: Environment Setup
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('4.1 Phase 1: Environment Setup', level=2)
    
    doc.add_paragraph('Install required Python packages:')
    
    install_cmd = """pip install tensorflow>=2.12.0 opencv-python>=4.8.0 numpy>=1.23.0 matplotlib>=3.7.0 scikit-learn>=1.2.0"""
    
    doc.add_paragraph(install_cmd, style='No Spacing')
    
    doc.add_paragraph()
    doc.add_paragraph('For voice feedback on Windows:')
    
    doc.add_paragraph('pip install pywin32', style='No Spacing')
    
    # ─────────────────────────────────────────────────────────────────────────
    # Phase 2: Emotion Model Training
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('4.2 Phase 2: Emotion Model Training', level=2)
    
    doc.add_heading('Step 2.1: Acquire Training Data', level=3)
    
    data_steps = [
        'Download FER-2013 or similar emotion dataset from Kaggle',
        'Organize into folder structure: data_large/train/{Angry,Fear,Happy,Sad,Neutral}/',
        'Minimum 3,000 images per class recommended',
        '17,000+ total images for best results',
        'Also create: data_large/test/ with same class structure',
    ]
    
    for step in data_steps:
        doc.add_paragraph(step, style='List Number')
    
    doc.add_heading('Step 2.2: Create Training Script', level=3)
    
    p = doc.add_paragraph()
    p.add_run('File: ').bold = True
    p.add_run('train_5class_v2.py')
    
    doc.add_paragraph()
    doc.add_paragraph('Key configuration parameters:')
    
    params = """
IMG_SIZE = 48
NUM_CLASSES = 5
BATCH_SIZE = 64
EPOCHS = 60
LR_INIT = 5e-4

EMOTION_LABELS = ['Angry', 'Fear', 'Happy', 'Sad', 'Neutral']
"""
    
    doc.add_paragraph(params, style='No Spacing')
    
    doc.add_heading('Step 2.3: Run Training', level=3)
    
    train_cmd = 'python train_5class_v2.py --train_dir data_large/train --test_dir data_large/test'
    
    doc.add_paragraph(train_cmd, style='No Spacing')
    
    doc.add_paragraph()
    
    doc.add_heading('Expected Results', level=3)
    
    results = [
        'Training accuracy: 75-80%',
        'Validation accuracy: 65-72%',
        'Best model saved to: emotion_model.keras',
        'Training curves saved to: training_curves_5class_v2.png',
        'Training time: 45-90 minutes (depending on hardware)',
    ]
    
    for result in results:
        doc.add_paragraph(result, style='List Bullet')
    
    doc.add_heading('Common Training Issues & Fixes', level=3)
    
    issues = [
        ('Model outputs Neutral for everything', 
         'Add label smoothing (0.1) and balanced class weights'),
        ('Happy confused with Sad', 
         'Add smile correction and increase brightness augmentation'),
        ('Overfitting (train acc >> val acc)', 
         'Increase dropout (0.50) and add L2 regularization (1e-4)'),
        ('Training stops too early (epoch 10)', 
         'Use larger dataset and proper cosine LR schedule'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Issue'
    hdr_cells[1].text = 'Fix'
    
    for issue, fix in issues:
        row_cells = table.add_row().cells
        row_cells[0].text = issue
        row_cells[1].text = fix
    
    doc.add_paragraph()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Phase 3: Gender Model Training
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('4.3 Phase 3: Gender Model Training', level=2)
    
    p = doc.add_paragraph()
    p.add_run('⚠ CRITICAL: ').bold = True
    p.add_run('Gender model MUST use UTKFace dataset for 95%+ accuracy.')
    
    doc.add_paragraph()
    
    doc.add_heading('Step 3.1: Download UTKFace Dataset', level=3)
    
    p = doc.add_paragraph('Visit: ')
    add_hyperlink(p, 'https://www.kaggle.com/datasets/nipunarora8/utkface-new', 
                  'https://www.kaggle.com/datasets/nipunarora8/utkface-new')
    
    download_steps = [
        'Create Kaggle account (free)',
        'Download ZIP file (~1.3 GB)',
        'Extract all images to: ./data_utkface/',
        'Verify files have format: age_gender_race_date.jpg',
    ]
    
    for step in download_steps:
        doc.add_paragraph(step, style='List Number')
    
    doc.add_heading('Step 3.2: Organize Dataset', level=3)
    
    p = doc.add_paragraph()
    p.add_run('File: ').bold = True
    p.add_run('download_utkface.py (provided in project)')
    
    doc.add_paragraph()
    doc.add_paragraph('Run:')
    doc.add_paragraph('python download_utkface.py', style='No Spacing')
    
    doc.add_paragraph()
    doc.add_paragraph('This creates organized structure:')
    
    structure = """
utkface_organized/
├── train/
│   ├── Male/    (70% of male images)
│   └── Female/  (70% of female images)
├── val/
│   ├── Male/    (15%)
│   └── Female/  (15%)
└── test/
    ├── Male/    (15%)
    └── Female/  (15%)
"""
    
    doc.add_paragraph(structure, style='No Spacing')
    
    doc.add_heading('Step 3.3: Train Gender Model', level=3)
    
    p = doc.add_paragraph()
    p.add_run('File: ').bold = True
    p.add_run('train_gender_model_utkface.py (provided)')
    
    doc.add_paragraph()
    doc.add_paragraph('Run:')
    doc.add_paragraph('python train_gender_model_utkface.py', style='No Spacing')
    
    doc.add_paragraph()
    
    doc.add_heading('Training Details', level=3)
    
    gender_train = [
        'Epochs: 50 with early stopping (patience=10)',
        'Batch size: 128',
        'Learning rate: 1e-3 with ReduceLROnPlateau',
        'Augmentation: rotation, shift, zoom, brightness',
        'Preprocessing: Histogram equalization on grayscale',
        'Expected accuracy: 92-95% validation',
        'Training time: 30-60 minutes',
        'Output: gender_model.keras (replaces any old version)',
    ]
    
    for detail in gender_train:
        doc.add_paragraph(detail, style='List Bullet')
    
    # ─────────────────────────────────────────────────────────────────────────
    # Phase 4: Real-Time Detector
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('4.4 Phase 4: Real-Time Detector Implementation', level=2)
    
    doc.add_paragraph(
        'Implement the main application that integrates all models for real-time detection.'
    )
    
    doc.add_heading('Core Components to Implement', level=3)
    
    components_impl = [
        'FastWebcamStream: Threaded camera capture with DirectShow',
        'GenderDetector: CNN inference with EMA smoothing',
        'GlassesDetector: Haar cascades + brightness analysis',
        'AsyncVoiceEngine: Background TTS with cooldown',
        'Main Loop: 30 FPS locked processing pipeline',
    ]
    
    for comp in components_impl:
        doc.add_paragraph(comp, style='List Number')
    
    doc.add_heading('Main Loop Architecture', level=3)
    
    main_loop = """
def main():
    # 1. Initialize all components
    stream = FastWebcamStream(src=0, width=1280, height=720).start()
    face_cascade = load_face_cascade()
    smile_cascade = load_smile_cascade()
    gender_detector = GenderDetector()
    glasses_detector = GlassesDetector()
    voice_engine = AsyncVoiceEngine(cooldown=4.0).start()
    emotion_model = tf.keras.models.load_model('emotion_model.keras')
    
    # 2. Frame timing for 30 FPS
    target_fps = 30.0
    frame_time = 1.0 / target_fps
    
    while True:
        loop_start = time.time()
        
        # 3. Capture frame
        ret, frame = stream.read()
        
        # 4. Convert to grayscale & enhance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_enhanced, is_low_light = auto_light(gray)
        
        # 5. Detect faces (every 2 frames for speed)
        if frame_count % 2 == 0:
            faces = face_cascade.detectMultiScale(...)
        
        # 6. Process each face
        for face_id, (x, y, w, h) in enumerate(faces):
            # Extract face ROI
            x0, y0, x1, y1 = expand_face_rect(x, y, w, h, ...)
            face_roi = gray_enhanced[y0:y1, x0:x1]
            
            # Emotion prediction
            raw_probs = emotion_model.predict(...)
            smile_score = detect_smile_score(smile_cascade, face_roi)
            final_probs = apply_smile_correction(raw_probs, smile_score)
            emotion = EMOTION_LABELS[np.argmax(final_probs)]
            
            # Gender prediction
            gender, gender_conf, _ = gender_detector.predict(face_roi, face_id)
            
            # Glasses detection
            glasses_type, glasses_conf = glasses_detector.detect(...)
            
            # Draw UI
            draw_face_badge(frame, ...)
            draw_gender_glasses_badge(frame, ...)
        
        # 7. Draw top bar & side panel
        draw_top_bar(frame, ...)
        draw_side_panel(frame, ...)
        
        # 8. Display
        cv2.imshow("Emotion Monitor Pro", frame)
        
        # 9. Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        # 10. FPS regulation
        elapsed = time.time() - loop_start
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
"""
    
    doc.add_paragraph(main_loop, style='No Spacing')
    
    doc.add_heading('Critical Implementation Details', level=3)
    
    p = doc.add_paragraph()
    p.add_run('Face Preprocessing: ').bold = True
    p.add_run('DO NOT apply histogram equalization during inference (causes domain shift)')
    
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.add_run('Face Margin: ').bold = True
    p.add_run('Use 2% expansion only (FACE_MARGIN = 0.02) to match tight training crops')
    
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.add_run('Smile Correction: ').bold = True
    p.add_run('Apply ONCE per prediction with gentle weights (0.08, 0.05, 0.15, 0.08)')
    
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.add_run('Temperature Scaling: ').bold = True
    p.add_run('Use T=0.85 to sharpen predictions (lower = sharper, higher = softer)')
    
    # ─────────────────────────────────────────────────────────────────────────
    # Phase 5: Testing
    # ─────────────────────────────────────────────────────────────────────────
    
    doc.add_heading('4.5 Phase 5: Testing & Validation', level=2)
    
    doc.add_heading('Test Checklist', level=3)
    
    test_categories = [
        ('Single Face', [
            'Emotion detection accurate (Happy when smiling, Sad when frowning)',
            'Gender correct (Male for male with beard, Female for female)',
            'Glasses detected (eyeglasses vs sunglasses)',
            'Stable labels (no jittery switching)',
        ]),
        ('Multi-Face (2-10 people)', [
            'All faces detected simultaneously',
            'Each face has unique Person # ID',
            'Performance stays at 30 FPS',
        ]),
        ('Lighting Conditions', [
            'Bright room: Clear detection',
            'Dark room: Night mode activates (yellow badge)',
            'Backlighting: Auto-enhancement compensates',
        ]),
        ('Edge Cases', [
            'Side profile (30° angle): Still detects',
            'Glasses on/off: Detection updates correctly',
            'Beard vs clean-shaven: Gender stays correct',
            'Hat/cap: Face still detected',
        ]),
        ('Performance', [
            'FPS counter shows 28-30 FPS consistently',
            'No lag when moving face',
            'Voice feedback has 4-second cooldown',
        ]),
    ]
    
    for category, items in test_categories:
        doc.add_heading(category, level=4)
        for item in items:
            doc.add_paragraph(f'☐ {item}', style='List Bullet')
    
    doc.add_page_break()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 5. DATASET ACQUISITION
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('5. Dataset Acquisition', level=1)
    
    doc.add_heading('Emotion Dataset (FER-2013 or FER+)', level=2)
    
    p = doc.add_paragraph('Source: ')
    add_hyperlink(p, 'https://www.kaggle.com/datasets/msambare/fer2013',
                  'Kaggle FER-2013')
    
    doc.add_paragraph()
    
    fer_details = [
        'Total images: 35,887 (28,709 train + 7,178 test)',
        'Image size: 48×48 grayscale',
        'Classes: 7 (collapse to 5 by using indices [0,2,3,4,6])',
        'Format: Grayscale face images pre-cropped',
        'Organization needed: Sort into folders by emotion class',
    ]
    
    for detail in fer_details:
        doc.add_paragraph(detail, style='List Bullet')
    
    doc.add_heading('Gender Dataset (UTKFace - REQUIRED)', level=2)
    
    p = doc.add_paragraph('Source: ')
    add_hyperlink(p, 'https://www.kaggle.com/datasets/nipunarora8/utkface-new',
                  'Kaggle UTKFace')
    
    doc.add_paragraph()
    
    utk_details = [
        'Total images: ~24,000',
        'Image size: Variable (will be resized to 64×64)',
        'Format: age_gender_race_date.jpg',
        'Gender encoding: 0=Male, 1=Female',
        'Age range: 0-116 years',
        'Ethnicities: White, Black, Asian, Indian, Other',
        'Download size: ~1.3 GB ZIP',
    ]
    
    for detail in utk_details:
        doc.add_paragraph(detail, style='List Bullet')
    
    doc.add_heading('Dataset Organization Steps', level=3)
    
    org_steps = [
        'Download ZIP from Kaggle',
        'Extract to ./data_utkface/',
        'Run: python download_utkface.py',
        'Verify organized structure created in ./utkface_organized/',
        'Check train/val/test splits (70/15/15)',
    ]
    
    for i, step in enumerate(org_steps, 1):
        doc.add_paragraph(f'{i}. {step}', style='List Number')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 6. PERFORMANCE OPTIMIZATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('6. Performance Optimization Tips', level=1)
    
    optimizations = [
        ('TensorFlow XLA Compilation', 
         'model.compile(..., jit_compile=True) for 10-20% speedup'),
        ('Reduce Face Detection Frequency',
         'Only detect every 2-3 frames: if frame_count % 2 == 0: detect_faces(...)'),
        ('Use Larger Cascade Scale Factor',
         'scaleFactor=1.25 instead of 1.10 (faster but less accurate)'),
        ('Batch Processing',
         'Collect multiple faces and predict as batch when available'),
        ('GPU Acceleration',
         'TensorFlow uses GPU automatically if available (verify with tf.config.list_physical_devices("GPU"))'),
        ('Reduce Resolution',
         'Use 640×480 instead of 1280×720 if FPS drops'),
        ('Increase minSize',
         'minSize=(80,80) instead of (60,60) to skip smaller faces'),
    ]
    
    for opt, desc in optimizations:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f'{opt}: ').bold = True
        p.add_run(desc)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 7. TROUBLESHOOTING
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('7. Troubleshooting Guide', level=1)
    
    troubles = [
        ('Cannot load model',
         'Ensure emotion_model.keras and gender_model.keras are in same directory as script'),
        ('Haar cascade not found',
         'OpenCV Haar cascades bundled with cv2.data module - verify path'),
        ('No camera detected',
         'Try different indices: FastWebcamStream(src=1) for external webcam'),
        ('Low FPS (15-20)',
         'Reduce resolution, skip frames, increase minSize in cascade'),
        ('Voice feedback not working',
         'Install pywin32: pip install pywin32'),
        ('Gender detection stuck',
         'Increase smoothing alpha: self.alpha = 0.60'),
        ('Emotion always Neutral',
         'Retrain with balanced class weights and label smoothing'),
        ('Happy detected as Sad',
         'Check smile correction applied only once with gentle weights'),
        ('Gender always Female',
         'Retrain on UTKFace dataset (not emotion dataset with pseudo-labels)'),
        ('Blurry in dark room',
         'Verify auto_light() function applies CLAHE + gamma correction'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Issue'
    hdr_cells[1].text = 'Solution'
    
    for issue, solution in troubles:
        row_cells = table.add_row().cells
        row_cells[0].text = issue
        row_cells[1].text = solution
    
    doc.add_paragraph()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 8. ADVANCED FEATURES
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('8. Advanced Features (Optional Extensions)', level=1)
    
    advanced = [
        ('Frustration Detection', 
         'Track sustained negative emotions (Angry/Sad > 5 seconds), trigger voice alert'),
        ('Fatigue Detection',
         'Monitor eye-closure frequency and blink rate, detect drowsiness'),
        ('Attention Monitoring',
         'Track gaze direction and face visibility, alert when looking away'),
        ('Multi-Camera Support',
         'Process multiple webcam streams simultaneously'),
        ('Recording & Playback',
         'Save sessions to video file using cv2.VideoWriter'),
        ('Data Logging',
         'Export emotion timeline to CSV for analysis'),
        ('Remote Monitoring',
         'Stream results over network (Flask/FastAPI backend)'),
    ]
    
    for feature, desc in advanced:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f'{feature}: ').bold = True
        p.add_run(desc)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 9. REFERENCES
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('9. References & Resources', level=1)
    
    doc.add_heading('Datasets', level=2)
    
    p = doc.add_paragraph('• FER-2013: ')
    add_hyperlink(p, 'https://www.kaggle.com/datasets/msambare/fer2013',
                  'https://www.kaggle.com/datasets/msambare/fer2013')
    
    p = doc.add_paragraph('• UTKFace: ')
    add_hyperlink(p, 'https://www.kaggle.com/datasets/nipunarora8/utkface-new',
                  'https://www.kaggle.com/datasets/nipunarora8/utkface-new')
    
    doc.add_heading('Research Papers', level=2)
    
    papers = [
        'Goodfellow et al. (2013): "Challenges in Representation Learning: A report on three machine learning contests"',
        'Taigman et al. (2014): "DeepFace: Closing the Gap to Human-Level Performance"',
        'He et al. (2016): "Deep Residual Learning for Image Recognition"',
    ]
    
    for paper in papers:
        doc.add_paragraph(paper, style='List Bullet')
    
    doc.add_heading('Libraries & Documentation', level=2)
    
    p = doc.add_paragraph('• TensorFlow: ')
    add_hyperlink(p, 'https://www.tensorflow.org/', 'https://www.tensorflow.org/')
    
    p = doc.add_paragraph('• OpenCV: ')
    add_hyperlink(p, 'https://docs.opencv.org/', 'https://docs.opencv.org/')
    
    p = doc.add_paragraph('• NumPy: ')
    add_hyperlink(p, 'https://numpy.org/', 'https://numpy.org/')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # APPENDIX: PROJECT FILE STRUCTURE
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_page_break()
    
    doc.add_heading('Appendix A: Project File Structure', level=1)
    
    file_structure = """
project/
│
├── realtime_detector.py                # Main application (run this)
├── train_5class_v2.py                  # Emotion model training script
├── train_gender_model_utkface.py       # Gender model training script
├── download_utkface.py                 # UTKFace dataset organizer
├── requirements.txt                    # Python dependencies
│
├── emotion_model.keras                 # Trained emotion model (48×48)
├── gender_model.keras                  # Trained gender model (64×64)
│
├── data_large/                         # Emotion training dataset
│   ├── train/
│   │   ├── Angry/
│   │   ├── Fear/
│   │   ├── Happy/
│   │   ├── Sad/
│   │   └── Neutral/
│   └── test/
│       └── (same structure)
│
├── data_utkface/                       # UTKFace raw images
│   └── *.jpg files
│
└── utkface_organized/                  # Organized train/val/test
    ├── train/
    │   ├── Male/
    │   └── Female/
    ├── val/
    │   ├── Male/
    │   └── Female/
    └── test/
        ├── Male/
        └── Female/
"""
    
    doc.add_paragraph(file_structure, style='No Spacing')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # APPENDIX: KEYBOARD SHORTCUTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('Appendix B: Keyboard Shortcuts (Runtime Controls)', level=1)
    
    shortcuts = [
        ('Q', 'Quit application'),
        ('V', 'Toggle voice feedback on/off'),
        ('T', 'Toggle dark/light theme'),
        ('E', 'Toggle quality enhancement (CLAHE sharpening)'),
        ('ESC', 'Emergency exit'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Colorful Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Key'
    hdr_cells[1].text = 'Action'
    
    for key, action in shortcuts:
        row_cells = table.add_row().cells
        row_cells[0].text = key
        row_cells[1].text = action
    
    # ═══════════════════════════════════════════════════════════════════════════
    # APPENDIX: EXPECTED PERFORMANCE METRICS
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_heading('Appendix C: Expected Performance Metrics', level=1)
    
    metrics = [
        ('Emotion Detection - Validation Accuracy', '65-72%'),
        ('Emotion Detection - Webcam Accuracy', '60-68% (domain shift)'),
        ('Emotion Detection - Inference Time', '8-12ms per face'),
        ('Gender Detection - Validation Accuracy', '92-95% (with UTKFace)'),
        ('Gender Detection - Webcam Accuracy', '90-93%'),
        ('Gender Detection - Inference Time', '4-6ms per face'),
        ('Glasses Detection - Accuracy', '85-90%'),
        ('Glasses Detection - Inference Time', '2-3ms per face'),
        ('Overall System - FPS', '28-30 (locked)'),
        ('Overall System - Latency', '<35ms (capture to display)'),
        ('Overall System - Max Faces', '9-10 simultaneously'),
        ('RAM Usage', '500-800 MB'),
        ('CPU Usage', '30-50% (single core, i5+)'),
    ]
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Medium Grid 1 Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Metric'
    hdr_cells[1].text = 'Expected Value'
    
    for metric, value in metrics:
        row_cells = table.add_row().cells
        row_cells[0].text = metric
        row_cells[1].text = value
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FOOTER: SUCCESS CRITERIA
    # ═══════════════════════════════════════════════════════════════════════════
    
    doc.add_page_break()
    
    doc.add_heading('Success Criteria Checklist', level=1)
    
    p = doc.add_paragraph()
    p.add_run('Your implementation is complete when all criteria are met:').bold = True
    
    doc.add_paragraph()
    
    criteria = [
        'Emotion detection works on webcam with 60%+ perceived accuracy',
        'Gender detection shows correct label for test subjects (90%+)',
        'Glasses detection distinguishes eyeglasses vs sunglasses',
        'System maintains 28-30 FPS with 1-5 faces',
        'UI is clean, responsive, and matches Apple design language',
        'Voice feedback provides helpful behavioral alerts',
        'All keyboard shortcuts work (Q, V, T, E)',
        'Dark room auto-lighting activates correctly',
        'Multi-face tracking assigns unique IDs',
        'Application runs without crashes for 30+ minutes',
        'Model files load correctly (emotion_model.keras, gender_model.keras)',
        'Smile correction prevents false Angry labels',
        'Gender predictions are stable (no jittery switching)',
    ]
    
    for criterion in criteria:
        doc.add_paragraph(f'☐ {criterion}', style='List Bullet')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SAVE DOCUMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    output_path = 'Emotion_Detection_System_Complete_Guide.docx'
    doc.save(output_path)
    print(f'\n[OK] Document created successfully!')
    print(f'[OK] Saved to: {output_path}')
    print(f'\n[INFO] Document contains:')
    print('  • Complete project overview')
    print('  • Technical requirements and architecture')
    print('  • Step-by-step implementation guide')
    print('  • Training configurations and code examples')
    print('  • Troubleshooting guide')
    print('  • Dataset acquisition instructions')
    print('  • Performance optimization tips')
    print('  • References and resources')
    print('\n[INFO] Total pages: ~25-30')
    print('[INFO] Ready for use in Google AI Studio or other AI development tools')
    
    return output_path

if __name__ == '__main__':
    create_emotion_detection_doc()
