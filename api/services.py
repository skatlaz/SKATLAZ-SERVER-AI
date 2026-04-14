from pathlib import Path
from db.feed import FeedRAG
from models.trainer import RAGTrainer
from db.database import Database

class AIService:
    def __init__(self):
        self.feed = FeedRAG("rag/feed")
        self.rag = RAGTrainer()
        self.db = Database()

    def ask(self, prompt):
        qid = self.db.save_question(prompt)
        feeds = self.feed.load_feeds()

        docs = [item.get("summary", "") for item in feeds]
        if not docs:
            return {"answer": "Nenhum feed encontrado em rag/feed/"}

        scores = self.rag.similarity_search(prompt, docs)
        idx = scores.argmax()
        best = feeds[idx]

        self.db.save_response(
            qid,
            best["source"],
            best["summary"],
            float(scores[idx])
        )

        return {
            "question": prompt,
            "answer": best["summary"],
            "source": best["source"],
            "score": float(scores[idx])
        }

    def feeds(self):
        return self.feed.load_feeds()

    def train(self, question, answer):
        self.db.cursor.execute(
            "INSERT INTO training_data (question, answer, source) VALUES (?, ?, ?)",
            (question, answer, "manual_train")
        )
        self.db.conn.commit()
        return {"status": "trained"}
