import kenlm

class language_detector:
    def __init__(self):
        self.latin_lang_model = kenlm.Model('../../kenlm/lm/latin_3gram.arpa')
        print("latin done")
        self.english_lang_model = kenlm.Model('../../kenlm/lm/english_3gram.arpa')
        print("english done")
    
    def predict(self, text):
        """
        True - latin, False - english
        """
        lm_score = self.latin_lang_model.score(text)
        em_score = self.english_lang_model.score(text)
        if lm_score > em_score:
            return True
        else:
            return False