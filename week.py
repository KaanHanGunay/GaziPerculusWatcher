class Week:
    def __init__(self, name):
        self.name = name
        self.links = []

    def __str__(self):
        return f'{self.name} toplam {len(self.links)} izlenmemiş ders tespit edilmiştir.'
