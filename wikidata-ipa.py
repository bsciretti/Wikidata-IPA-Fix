import pywikibot, time
from pywikibot.data.sparql import SparqlQuery

def fix_ipa_transcription(page_id="Q4115189", test_mode=True):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    if page_id.startswith("L"):
        page_id_workingon = page_id.split("-")[0]
        item = pywikibot.LexemePage(repo, page_id_workingon)
        item.get()
        modified = False
        
        for form in item.forms:
            if "P898" in form.claims:
                for claim in form.claims["P898"]:
                    old_value = claim.getTarget()
                    new_value = old_value.replace("'", "ˈ").replace("g", "ɡ").replace(":","ː")
                    
                    if old_value != new_value:
                        if test_mode and page_id != "Q4115189":
                            print(f"[TEST] Modificherebbe: {page_id_workingon} (forma {form.id}): {old_value} -> {new_value}")
                            time.sleep(1)
                        else:
                            claim.changeTarget(new_value, summary="Correzione automatica della trascrizione IPA (' → ˈ, g → ɡ, : → ː)")
                            print(f"Modificato: {page_id} (forma {form.id}): {old_value} -> {new_value}")
                            modified = True
        
        if not modified:
            print(f"Nessuna modifica necessaria per {page_id}.")
    else:
        item = pywikibot.ItemPage(repo, page_id)
        item.get()
        prop_id = "P898"  # Proprietà Trascrizione IPA
        
        if prop_id in item.claims:
            for claim in item.claims[prop_id]:
                old_value = claim.getTarget()
                new_value = old_value.replace("'", "ˈ").replace("g", "ɡ").replace(":","ː")
                
                if old_value != new_value:
                    if test_mode and page_id != "Q4115189":
                        print(f"[TEST] Modificherebbe: {page_id}: {old_value} -> {new_value}")
                    else:
                        claim.changeTarget(new_value, summary="Correzione automatica della trascrizione IPA (' → ˈ, g → ɡ)")
                        print(f"Modificato: {page_id}: {old_value} -> {new_value}")
                else:
                    print(f"Nessuna modifica necessaria per {page_id}.")
        else:
            print(f"L'elemento {page_id} non ha la proprietà {prop_id}.")

def process_all_ipa_items():
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    query = '''SELECT ?item WHERE { ?item wdt:P898 ?ipa . FILTER(CONTAINS(?ipa, "'") || CONTAINS(?ipa, "g") || CONTAINS(?ipa, ":")) }'''  
    sparql = SparqlQuery()
    generator = sparql.get_items(query)
    
    for item_id in generator:
        try:
            fix_ipa_transcription(item_id, test_mode=True)
        except Exception as e:
            print(f"Errore su {item_id}: {e}")

if __name__ == "__main__":
    process_all_ipa_items()
