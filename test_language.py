from language import detect_language


test_queries = [
    "Will it rain tomorrow?",
    "क्या कल बारिश होगी?",
    "ગુજરાતીમાં વરસાદ પડશે?",
    "मराठीत पाऊस पडेल का?",
    "ਪੰਜਾਬ ਵਿੱਚ ਮੌਸਮ ਕਿਵੇਂ ਹੈ?",
    "நாளை மழை பெய்யுமா?",
    "రేపు వర్షం పడుతుందా?",
    "ಮಳೆ ಬೀಳುತ್ತದೆಯೇ?",
    "बांग्लায় আবহাওয়া কেমন?",
    "ଓଡ଼ିଶାରେ ପାଗ କେମିତି?"
]


print("=" * 50)
print("LANGUAGE MODEL TEST")
print("=" * 50)

for query in test_queries:
    language = detect_language(query)

    print()
    print("Query:", query)
    print("Language:", language)