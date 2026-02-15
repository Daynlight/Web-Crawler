<div align=center>

# Web-Crawler

</div>

Napisz prostego web crawlera, który dla zadanej strony tematu na Wikipedii wypisze wszystkie strony Wikipedii osiągalne przez sekcję “See also”.

Wymagania:

- [x] Start z jednego podanego URL (np. hasło na en.wikipedia.org).
- [x] Dla każdej odwiedzanej strony pobierz linki z sekcji See also i przechodź dalej wgłąb.
- [x] Przeszukiwanie bez powtórzeń (nie odwiedzaj tej samej strony drugi raz).
- [x] Implementacja iteracyjna (kolejka/stos) – bez rekurencji.
- [x] Na końcu wypisz maksymalną głębokość, którą udało się osiągnąć.