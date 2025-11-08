import os


class Config:
    # API Configuration
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    # arXiv Configuration
    ARXIV_MAX_RESULTS = 5
    ARXIV_CATEGORIES = [
        'quant-ph',  # Quantum Physics
        'cond-mat.mes-hall',  # Mesoscale and Nanoscale Physics
        'physics.atom-ph',  # Atomic Physics
    ]

    # Search Configuration
    MAX_SEARCH_RESULTS = 10
    FUSION_WEIGHTS = {
        'arxiv': 0.4,
        'serpapi': 0.35,
        'google': 0.25
    }

    # Quantum Keywords
    QUANTUM_KEYWORDS = [
        'quantum', 'qubit', 'entanglement', 'superposition',
        'decoherence', 'quantum computing', 'quantum mechanics',
        'quantum algorithm', 'quantum gate', 'quantum circuit',
        'quantum error correction', 'quantum cryptography',
        'quantum teleportation', 'bell state', 'bloch sphere',
        'hamiltonian', 'schrodinger', 'heisenberg', 'pauli',
        'quantum annealing', 'quantum supremacy', 'qiskit',
        'quantum information', 'quantum field theory'
    ]