from typing import List, Dict
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
import re


class RAGEngine:
    """Simple RAG Engine without ChromaDB - No compilation needed!"""

    def __init__(self, groq_api_key: str = None):
        print("[RAG] Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        self.documents = []
        self.embeddings = []

        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')

        if self.groq_api_key:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
                self.llm_available = True
                self.model_name = "llama-3.3-70b-versatile"
                print(f"[RAG] ✓ Groq LLM ready (model: {self.model_name})")
            except Exception as e:
                print(f"[RAG] ⚠ Groq init error: {e}")
                self.llm_available = False
                self.model_name = None
        else:
            self.groq_client = None
            self.llm_available = False
            self.model_name = None
            print("[RAG] ⚠ No GROQ_API_KEY found")

    def add_documents(self, documents: List[Dict]):
        if not documents:
            return

        self.documents = []
        texts = []

        for i, doc in enumerate(documents):
            text = f"{doc['title']}. {doc['snippet']}"
            texts.append(text)

            self.documents.append({
                'id': i,
                'text': text,
                'metadata': {
                    'title': doc['title'],
                    'link': doc['link'],
                    'source': doc.get('source_type', doc.get('source', 'Unknown'))
                }
            })

        print("[RAG] Generating embeddings...")
        self.embeddings = self.embedder.encode(texts, show_progress_bar=False)
        print(f"[RAG] ✓ Indexed {len(documents)} documents")

    def retrieve(self, query: str, top_k: int = 8) -> List[Dict]:
        if not self.documents:
            return []

        query_embedding = self.embedder.encode([query], show_progress_bar=False)
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]

        retrieved_docs = []
        for idx in top_indices:
            retrieved_docs.append({
                'text': self.documents[idx]['text'],
                'metadata': self.documents[idx]['metadata'],
                'similarity': float(similarities[idx])
            })

        print(f"[RAG] ✓ Retrieved {len(retrieved_docs)} relevant documents")
        return retrieved_docs

    def generate_answer(self, query: str, retrieved_docs: List[Dict]) -> Dict:
        if self.llm_available:
            return self._generate_with_groq(query, retrieved_docs)
        else:
            return self._generate_template_based(query, retrieved_docs)

    def _generate_with_groq(self, query: str, retrieved_docs: List[Dict]) -> Dict:
        """Generate answer using Groq cloud LLM"""

        context_parts = []
        sources = []

        for i, doc in enumerate(retrieved_docs[:6], 1):
            source_name = doc['metadata']['source']
            context_parts.append(f"[Source {i} - {source_name}]\n{doc['text'][:600]}")
            sources.append({
                'title': doc['metadata']['title'],
                'link': doc['metadata']['link'],
                'type': source_name
            })

        context = "\n\n".join(context_parts)

        prompt = f"""You are an expert quantum computing educator.

Question: {query}

Sources:
{context}

Provide a comprehensive answer with:

MAIN DEFINITION:
[2-3 clear sentences]

KEY PROPERTIES:
- Property 1: [detailed explanation]
- Property 2: [detailed explanation]
- Property 3: [detailed explanation]
- Property 4: [detailed explanation]

Answer:"""

        try:
            print(f"[RAG] 🤖 Generating with Groq ({self.model_name})...")

            response = self.groq_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a quantum physics expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                top_p=0.9
            )

            if not response or not hasattr(response, 'choices') or not response.choices:
                print("[RAG] ⚠ Invalid response from Groq")
                return self._generate_template_based(query, retrieved_docs)

            answer_text = response.choices[0].message.content

            if not answer_text:
                print("[RAG] ⚠ Empty answer from Groq")
                return self._generate_template_based(query, retrieved_docs)

            # Parse answer
            structured = self._parse_llm_answer(answer_text, sources)

            print(f"[RAG] ✓ Answer generated ({len(answer_text)} chars)")

            return {
                'structured_answer': structured,
                'sources': sources,
                'confidence': 0.92,
                'generated_by': f'Groq AI ({self.model_name})'
            }

        except Exception as e:
            print(f"[RAG] ⚠ Groq error: {type(e).__name__}: {e}")
            return self._generate_template_based(query, retrieved_docs)

    def _generate_template_based(self, query: str, retrieved_docs: List[Dict]) -> Dict:
        if not retrieved_docs:
            return {
                'structured_answer': None,
                'sources': [],
                'confidence': 0.0,
                'generated_by': 'template'
            }

        best_doc = retrieved_docs[0]
        main_text = best_doc['text'][:800]

        properties = []
        sources = []
        source_types_seen = set()

        for doc in retrieved_docs[:10]:
            metadata = doc['metadata']
            source_type = metadata['source']

            sources.append({
                'title': metadata['title'],
                'link': metadata['link'],
                'type': source_type
            })

            if doc != retrieved_docs[0]:
                if source_type not in source_types_seen or len(properties) < 4:
                    sentences = doc['text'].split('. ')
                    prop_text = '. '.join(sentences[:3])
                    if not prop_text.endswith('.'):
                        prop_text += '.'

                    if len(prop_text) > 60:
                        properties.append({
                            'content': prop_text[:600],
                            'source': source_type,
                            'source_link': metadata['link'],
                            'source_title': metadata['title']
                        })
                        source_types_seen.add(source_type)

            if len(properties) >= 6:
                break

        structured = {
            'main': {
                'content': main_text,
                'source': best_doc['metadata']['source'],
                'source_link': best_doc['metadata']['link'],
                'source_title': best_doc['metadata']['title']
            },
            'properties': properties
        }

        return {
            'structured_answer': structured,
            'sources': sources[:12],
            'confidence': 0.72,
            'generated_by': 'template (fallback)'
        }

    def _parse_llm_answer(self, answer_text: str, sources: List[Dict]) -> Dict:
        """Parse LLM-generated answer into structured format - FIXED VERSION"""

        if not answer_text:
            answer_text = "No answer generated"

        # Remove markdown bold formatting (** characters)
        answer_text_clean = answer_text.replace('**', '')

        # Extract main definition
        main_match = re.search(
            r'MAIN DEFINITION:?\s*(.+?)(?=KEY PROPERTIES|KEY CONCEPTS|$)',
            answer_text_clean,
            re.DOTALL | re.IGNORECASE
        )

        if main_match:
            main_content = main_match.group(1).strip()
        else:
            paragraphs = [p.strip() for p in answer_text_clean.split('\n\n') if p.strip()]
            main_content = paragraphs[0] if paragraphs else answer_text_clean[:700]

        # Extract key properties
        properties_match = re.search(
            r'KEY PROPERTIES|KEY CONCEPTS:?\s*(.+)',
            answer_text_clean,
            re.DOTALL | re.IGNORECASE
        )

        properties = []
        if properties_match and properties_match.group(1):
            props_text = properties_match.group(1).strip()

            if props_text:  # Make sure it's not None or empty
                # Extract bullet points
                prop_lines = re.findall(
                    r'[-•]\s*Property\s*\d+:?\s*(.+?)(?=\n[-•]|\n\nProperty|$)',
                    props_text,
                    re.DOTALL | re.IGNORECASE
                )

                # If no "Property X:" format, try simpler pattern
                if not prop_lines:
                    prop_lines = re.findall(
                        r'[-•]\s*(.+?)(?=\n[-•]|\n\n|$)',
                        props_text,
                        re.DOTALL
                    )

                for i, prop in enumerate(prop_lines[:8]):
                    prop_clean = ' '.join(prop.strip().split())
                    if len(prop_clean) > 50:
                        source = sources[min(i, len(sources) - 1)] if sources else {
                            'type': 'Generated',
                            'link': '#',
                            'title': 'AI Generated'
                        }
                        properties.append({
                            'content': prop_clean[:600],
                            'source': source['type'],
                            'source_link': source['link'],
                            'source_title': source['title']
                        })

        # Fallback: extract paragraphs if no properties found
        if not properties:
            paragraphs = [p.strip() for p in answer_text_clean.split('\n\n') if p.strip()]
            for i, para in enumerate(paragraphs[1:7]):
                if len(para) > 60 and not para.upper().startswith('MAIN DEFINITION'):
                    source = sources[min(i, len(sources) - 1)] if sources else {
                        'type': 'Generated',
                        'link': '#',
                        'title': 'AI'
                    }
                    properties.append({
                        'content': para[:600],
                        'source': source['type'],
                        'source_link': source['link'],
                        'source_title': source['title']
                    })

        return {
            'main': {
                'content': main_content[:900],
                'source': sources[0]['type'] if sources else 'Generated',
                'source_link': sources[0]['link'] if sources else '#',
                'source_title': sources[0]['title'] if sources else 'Answer'
            },
            'properties': properties
        }

    def reset(self):
        self.documents = []
        self.embeddings = []