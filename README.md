# Optymalizator Planu Zajęć
Program służący do układania optymalnego planu zajęć dla szkoły/uczelni z wykorzystaniem kolorowania grafu.

### Autorzy
- Mikołaj Krakowiak
- Jakub Kozłowski

### Podstawy teoretyczne

Układanie planu zajęć jest bardzo ważnym zadaniem realizowanym przez zarządzających dowolną szkołą czy uczelnią. Bez takiego planu trudno wyobrazić sobie pracę instytucji edukacyjnej. Obecnie, zależnie od rodzaju szkoły, plan zajęć jest przygotowywany tylko raz (szkoła podstawowa, gimnazjum) lub więcej razy (liceum ogólnokształcące) w roku szkolnym. Inaczej natomiast będzie w przyszłości, co możemy zauważyć uwzględniając ustalenia reformy systemów edukacji i zatrudniania nauczycieli. Zadanie ułożenia wystarczająco dobrego planu lekcji, w zależności od rozmiaru szkoły i umiejętności układającego, wymaga poświęcenia pracy trwającej od kilku dni do dwóch tygodni, który to czas mógłby być przeznaczony na inne cele. Od momentu nastania ery komputeryzacji naszego życia, a także w ostatnich latach komputeryzacji szkół, pojawiło się wiele komputerowych programów wspomagających układanie planu lekcji. Programy takie są lepsze lub gorsze, bardziej lub mniej przyjazne dla użytkownika, dające w wyniku bardziej lub mniej doskonałe plany. Często zależy to od specyfiki danej instytucji lub od algorytmu użytego do stworzenia programu.

Zadanie układania harmonogramu zajęć ma bardzo ważne praktyczne zastosowania. Było bardzo intensywnie badane i udowodniono, że jest ono NP-trudne. Jest tak z powodu wielu występujących w zadaniu nietrywialnych ograniczeń o różnym charakterze. Pokazano już bardzo wiele algorytmów wykorzystujących znane obszary dziedziny badań operacyjnych i adaptujących nowe. Pierwsze algorytmy zastosowane i wykonywane przy pomocy komputera pojawiły się już we wczesnych latach sześćdziesiątych. W proponowanych przez siebie metodach rozwiązywania problemu układania planu lekcji badacze wykorzystują bardzo często różnego rodzaju algorytmy kolorowania grafu, gdyż jedną z postaci problemu jest graf, przy pomocy którego łatwo można przedstawić konflikty między poszczególnymi zajęciami, klasami czy nauczycielami. Korzysta się również z metod sekwencyjnych. Przeniesienie zachowań organizmów biologicznych na grunt algorytmów pozwoliło, przy rozwiązywaniu omawianego problemu, na zastosowanie algorytmów genetycznych. Używane są również metody lokalnego przeglądu, na przykład symulowanego wyżarzania, metody przeglądu z listą zakazów. Niezmiernie rozprzestrzenione jest podejście hybrydowe, w którym stosowane są algorytmy różnych rodzajów nawzajem się uzupełniających.

Najważniejszym celem niniejszej pracy jest zaprezentowanie algorytmu układania szkolnego planu lekcji, w którym w jednym z etapów wykorzystywane jest kolorowanie grafu. Głównym zadaniem proponowanej metody jest układanie jak najlepszego szkolnego planu lekcji w rozsądnym, z powodów praktycznych, czasie przy uwzględnieniu występujących ograniczeń.

### Etapy procesu układaniu planu zajęć
1. Przekształcenie programu nauczania szkoły do postaci grafu
2. Kolorowanie grafu 
3. Przekształcenie pokolorowanego grafu na plan lekcji

### Przekształcenie programu nauczania szkoły do postaci grafu

W pierwszym kroku przekształcamy program nauczania znajdujący się w tabeli do postaci grafu w następujący sposób:
- każda godzina zajęć jest reprezentowana przez jeden wierzchołek grafu
- każde dwa wierzchołki reprezentujące godziny znajdujące się w tej samej kolumnie tabeli są połączone gałęzią, analogicznie mamy dla godzin z tego samego wiersza

Przykładowe programy nauczania obsługiwane przez nasz program (w nawiasach numery wierzchołków grafu):
![program_nauczania](https://user-images.githubusercontent.com/79112577/225261584-0dd613f6-5cf3-42ee-92b8-b3df2b5e7cb3.png)

Graf reprezentujący programy nauczania przedstawione powyżej:
<p align="center">
 <img src="https://pw20we.cs.put.poznan.pl/lib/exe/fetch.php?cache=&w=797&h=141&tok=9a4deb&media=ok21:s148157:program_nauczania.png">
</p>

