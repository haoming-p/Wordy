import nltk
nltk.data.path.append('./nltk_data')
from nltk.corpus import wordnet as wn

def nltk_relationnship(word):
    # Returns a list of the top N names for synsets
    def get_top_synset_name(synsets, n=3):
        sorted_synsets = sorted(synsets, key=lambda synset: sum(lemma.count() for lemma in synset.lemmas()), reverse=True)
        return [synset.name().split('.')[0] for synset in sorted_synsets[:n]]
    
    def get_all_synset_name(synsets):
        return [synset.name() for synset in synsets]
    
    # Returns a list of the top N lemma names
    def get_top_lemma_name(synsets, n=3):
        lemmas = [lemma for synset in synsets for lemma in synset.lemmas()]
        sorted_lemmas = sorted(lemmas, key=lambda lemma: lemma.count(), reverse=True)
        return [lemma.name() for lemma in sorted_lemmas[:n]]
    
    def get_all_lemma_name(synsets):
        return [lemma.name() for synset in synsets for lemma in synset.lemmas()]

    all_results = []
    synsets = wn.synsets(word) 
    for synset in synsets:    
        synset_result = {
            'synset': synset.name(),
            'definition': synset.definition(),
            'example': {
                'top': synset.examples()[0] if synset.examples() else '',
                'all': synset.examples(),
            },
            'synonym': {
                'top': get_top_lemma_name([synset]),  
                'all': get_all_lemma_name([synset])   
            },
            'hypernyms': {
                'top': get_top_synset_name(synset.hypernyms()),
                'all': get_all_synset_name(synset.hypernyms())
            },
            'hyponyms': {
                'top': get_top_synset_name(synset.hyponyms()),
                'all': get_all_synset_name(synset.hyponyms())
            },
            'siblings': {
                'top': get_top_synset_name(synset.hypernyms()[0].hyponyms()) if synset.hypernyms() else [],
                'all': get_all_synset_name(synset.hypernyms()[0].hyponyms()) if synset.hypernyms() else []
            },
            'metonym': {
                'top': get_top_synset_name(synset.part_meronyms()),
                'all': get_all_synset_name(synset.part_meronyms())
            },
        }
        all_results.append(synset_result)
        
    return all_results

# Example usage
if __name__ == "__main__":
    word = "dog"
    results = nltk_relationnship(word)
    import json
    print(json.dumps(results, indent=4, ensure_ascii=False))


