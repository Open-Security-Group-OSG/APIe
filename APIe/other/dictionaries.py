regex = {
    "binaryedge": r'\w{8}-[\w-]{14}-\w{12}(?!:)',
    "censys": r'\w{8}-[\w-]{14}-\w{12}:\w{32}',
    "fofa": r'^\b[^@]{1,64}@[^@]+\.[^@]+:\w{32}',
    "shodan": r'(?=^[^:]*$)\b\w{32}\b',
    "virustotal": r'\b\w{64}\b',
}
