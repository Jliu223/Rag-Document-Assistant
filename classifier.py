# classifier.py
# Simple PyTorch text classifier for document type prediction

import json
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import TfidfVectorizer


DATA_PATH = Path("data/training_data.json")
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "document_classifier.pth"


class DocumentClassifier(nn.Module):
    def __init__(self, input_size: int, num_classes: int):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.network(x)


def load_training_data() -> Tuple[List[str], List[str]]:
    """Load labeled document examples from JSON."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing training data file: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        records = json.load(file)

    texts = [item["text"] for item in records]
    labels = [item["label"] for item in records]

    return texts, labels


def train_classifier() -> Dict:
    """
    Train a small PyTorch classifier on TF-IDF document features.

    This is intentionally lightweight so it can run when the Streamlit app starts.
    For a larger project, you would move training into a separate train.py script.
    """
    texts, labels = load_training_data()

    label_names = sorted(list(set(labels)))
    label_to_id = {label: index for index, label in enumerate(label_names)}
    id_to_label = {index: label for label, index in label_to_id.items()}

    vectorizer = TfidfVectorizer(
        max_features=500,
        stop_words="english",
        lowercase=True,
    )

    X = vectorizer.fit_transform(texts).toarray()
    y = torch.tensor([label_to_id[label] for label in labels], dtype=torch.long)

    X_tensor = torch.tensor(X, dtype=torch.float32)

    model = DocumentClassifier(
        input_size=X_tensor.shape[1],
        num_classes=len(label_names),
    )

    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    model.train()

    for _ in range(250):
        predictions = model(X_tensor)
        loss = loss_fn(predictions, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    MODEL_DIR.mkdir(exist_ok=True)

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "label_names": label_names,
        },
        MODEL_PATH,
    )

    return {
        "model": model,
        "vectorizer": vectorizer,
        "id_to_label": id_to_label,
    }


def predict_document_type(text: str, classifier_bundle: Dict) -> str:
    """Predict document type from extracted PDF text."""
    model = classifier_bundle["model"]
    vectorizer = classifier_bundle["vectorizer"]
    id_to_label = classifier_bundle["id_to_label"]

    X = vectorizer.transform([text]).toarray()
    X_tensor = torch.tensor(X, dtype=torch.float32)

    model.eval()

    with torch.no_grad():
        logits = model(X_tensor)
        predicted_id = torch.argmax(logits, dim=1).item()

    return id_to_label[predicted_id]
