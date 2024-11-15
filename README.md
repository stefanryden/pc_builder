PC Byggare Pro
Beskrivning

PC Byggare Pro är ett Streamlit-baserat verktyg för att hjälpa dig bygga din egen dator genom att välja kompatibla komponenter och analysera priser. Verktyget erbjuder också integration med Tradera för att visa auktioner och köp-nu erbjudanden.
Funktioner

    Välj grafikkort och hitta kompatibla komponenter (moderkort, CPU, RAM, etc.).
    Analysera priset på nya och begagnade delar.
    Visualisera prisjämförelser mellan komponenter.
    Exportera din byggkonfiguration som CSV.
    Visa Tradera-listningar för dina valda komponenter.

Installation och körning
Lokalt
Förutsättningar

    Python 3.9 eller senare
    Pip

Steg

    Klona projektet:

git clone https://github.com/ditt-repo/pc_builder_pro.git
cd pc_builder_pro

Skapa och aktivera en virtuell miljö:

python -m venv venv
source venv/bin/activate  # På Windows: .\venv\Scripts\activate

Installera beroenden:

pip install -r requirements.txt

Kör applikationen:

streamlit run main.py

Öppna i webbläsaren: Applikationen körs på:

    http://localhost:8501

Körning med Docker
Förutsättningar

    Docker installerat och igång

Steg

    Bygg Docker-bilden: Kör följande kommando i projektets rotmapp (där Dockerfile finns):

docker build -t pc_builder_pro .

Kör Docker-containern: Starta containern med:

docker run -p 8501:8501 pc_builder_pro

Öppna i webbläsaren: Applikationen blir tillgänglig på:

    http://localhost:8501

Struktur

    main.py: Huvudskriptet för applikationen.
    requirements.txt: Lista över beroenden.
    Dockerfile: Instruktioner för att bygga Docker-bilden.
    data/: Innehåller komponentdatafiler.
    utils/: Innehåller hjälpfunktioner som komponentkompatibilitet och Tradera-integration.

Felsökning
Vanliga problem

    Streamlit-applikationen startar inte:
        Kontrollera att alla beroenden är installerade.
        Kontrollera att data/component_data.json finns på rätt plats.

    Docker-bygget misslyckas:
        Se till att Docker är installerat och igång.
        Kontrollera att Dockerfile och requirements.txt finns i projektets rotmapp.

    Kan inte se applikationen i webbläsaren:
        Kontrollera att port 8501 inte är upptagen.
        Kontrollera Docker-loggar:

        docker logs [CONTAINER_ID]

Bidra

    Öppna en "issue" i GitHub-repot om du stöter på problem eller har förslag på förbättringar.
    Skicka in pull requests för nya funktioner eller buggfixar.