from deepface import DeepFace

image_path = "test.jpg"

result = DeepFace.analyze(
    img_path=image_path,
    actions=["emotion"],
    enforce_detection=False
)

print(result)