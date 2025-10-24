from app.api.qr_code_recognize.image_enhancement import BinarizationEnhancement, UpscaleEnhancement

qr_code_enhancement_pipeline = [
    BinarizationEnhancement(),
    UpscaleEnhancement(scale_factor=2.0),
    UpscaleEnhancement(scale_factor=4.0),
]
