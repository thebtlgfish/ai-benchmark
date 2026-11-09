import os
import json
import time
import dotenv
from datasets import load_dataset
from message_handler import ask, usage

dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("Api Key Not Found")

os.makedirs("answers", exist_ok=True)

test_data = load_dataset("openai/gsm8k", "main", split="test")

models = [
    "beam",
    "gemma4:31b",
    "gpt-oss:120b",
    "gpt-oss:20b",
    "nemotron-3-nano:30b",
    "nemotron-3-super",
    "nemotron-3-ultra",
]


def benchmark(model):
    usage_left = float(usage(api_key))
    if usage_left < 10:
        print("Usage Left Is Too Low")
        exit()

    path = f"answers/{model.replace(':', '-')}_model_answers.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump([], f)

    start = time.perf_counter()

    for num, item in enumerate(test_data, 1):
        question = item["question"]
        expected = item["answer"].split("####")[-1].strip()

        time.sleep(1)
        answer = ask(
            model,
            api_key,
            question + "\nEnd your response with 'Answer: <number>'.",
        )
        print(f"{model} Answered Question #{num}")

        with open(path, encoding="utf-8") as f:
            results = json.load(f)

        results.append({
            "question": question,
            "expected": expected,
            "answer": answer,
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    minutes, seconds = divmod(time.perf_counter() - start, 60)
    print(f"{model} finished in {int(minutes)}m {seconds:.1f}s")


for model in models:
    benchmark(model)
