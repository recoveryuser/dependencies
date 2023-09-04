from skllm import MultiLabelZeroShotGPTClassifier
from skllm.config import SKLLMConfig

restaurant_reviews = [
    "The food was delicious and the service was excellent. A wonderful dining experience!",
    "The restaurant was in a great location, but the food was just average.",
    "The service was very slow and the food was cold when it arrived. Not a good experience.",
    "The restaurant has a beautiful ambiance, and the food was superb.",
    "The food was great, but I found it to be a bit overpriced.",
    "The restaurant was conveniently located, but the service was poor.",
    "The food was not as expected, but the restaurant ambiance was really nice.",
    "Great food and quick service. The location was also very convenient.",
    "The prices were a bit high, but the food quality and the service were excellent.",
    "The restaurant offered a wide variety of dishes. The service was also very quick."
]

restaurant_review_labels = [
    ["Food", "Service"],
    ["Location", "Food"],
    ["Service", "Food"],
    ["Atmosphere", "Food"],
    ["Food", "Price"],
    ["Location", "Service"],
    ["Food", "Atmosphere"],
    ["Food", "Service", "Location"],
    ["Price", "Food", "Service"],
    ["Food Variety", "Service"]
]

new_restaurant_reviews = [
    "The food was excellent and the restaurant was located in the heart of the city.",
    "The service was slow and the food was not worth the price.",
    "The restaurant had a wonderful ambiance, but the variety of dishes was limited."
]

SKLLMConfig.set_openai_key("any string")
SKLLMConfig.set_openai_org("any string")
# Initialize the classifier with the OpenAI model
clf = MultiLabelZeroShotGPTClassifier(openai_model="gpt4all::/Users/sindhu/.cache/gpt4all/ggml-model-gpt4all-falcon-q4_0.bin", max_labels=3)

# Train the model 
clf.fit(X=restaurant_reviews, y=restaurant_review_labels)

# Use the trained classifier to predict the labels of the new reviews
predicted_restaurant_review_labels = clf.predict(X=new_restaurant_reviews)

for review, labels in zip(new_restaurant_reviews, predicted_restaurant_review_labels):
    print(f"Review: {review}\nPredicted Labels: {labels}\n\n")

