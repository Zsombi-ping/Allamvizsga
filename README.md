# Allamvizsga

Python szkriptek feladata(Programs könyvtár):


  - Ast_traversal_B_file.py: Bigramok kinyerése forrásállomány egységben 
  - Extract_H_file.py: Kézi jellemzők kinyerésére forrásállomány egységben 
  - Extract_U_B_H_func.py: Unigramok, Bigramok és kézi jellemzők kinyerése függvény egységben 
  - Extract_U_file.py: Unigramok kinyerése forrásállomány egységben
  - Extract_bigrams_all_func.py: Bigramok kinyerése függvény egységben
  - Handcrafted_features_function.py: Kézi jellemzők kinyerése függvény egységben
  - bigrams_file_all.py: Bigramok kinyerése forrásállomány egységben
  - bigrams_indent.py: Segéd szkript amellyel a függvény szintű bigramokat vizsgáljuk
  - normalize.py: Eredményhalmaz normalizálása és a legfontosabb jellemzők kimutatása
  - KfoldCrossVal.py: Azonosítás során használt 3-réteges keresztvalidáció
  - oneClassSVM.py: Ellnőrzés során használt egyosztályos tartovektorgép (SVM), ROC görbe kirajzolása
  - interface.py: Felhasználói felület indítása, mérések elvégzése
  - settings.py: útvonalak, konstans értékek tártolása, beállítása
  
Szöveges állományok (TXT könyvtár): Jellemzők kinyerésére szolgáló segéd állományok

Diagrammok megjelenítéséért felelős szkriptek (Plots könyvtár):

  - barplot.py: Mérési eredmények összehasonlítása jellemző kategóriákra lebontva és ezek szemléltetése (Függvény és Forrásállomány)
  - boxplot.py: Unigramok és bigramokra kapott értékek ellenőrzés során (100 szerző és összes szerző)
  - histogram.py: Szavak mennyiségének az eloszlása átlagolva szerzőnként (9 forrásállomány szerzőnként)
  - pieplot.py: Első 10 legdiszkriminatívabb jellemző és ezek aránya (unigram és kézi jellemzők)
  
Eredményhalmazok (CSV könyvtár):

  -Minden jellemző kategóriára külön eredményhalmaz van (forrásállomány és függvény esetén), valamint ezek egyesítése is megtalálható.
