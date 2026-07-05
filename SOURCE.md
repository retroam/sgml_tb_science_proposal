# Source model handoff notes

## Candidate model

- BioModels accession: `BIOMD0000000151`
- Title: `Singh2006_IL6_Signal_Transduction`
- BioModels page: <https://www.ebi.ac.uk/biomodels/BIOMD0000000151>
- Biology: IL-6 signal transduction with JAK/STAT and related signaling in hepatocytes.
- Modeling approach: deterministic ODE SBML model.
- Publication: Singh, Jayaraman, and Hahn, 2006, Biotechnology and Bioengineering, PubMed `16752369`.

## License status from prior work

Prior proposal work observed the BioModels entry as curated and recorded the encoded model license as CC0 Public Domain Dedication. The final task still needs entry-specific metadata captured from the SBML or current BioModels page at packaging time.

## Known BioModels access issue

Prior work could reach the BioModels page but BioModels download endpoints returned HTTP 403 for the proposal orb, so no verified SBML checksum was recorded. This handoff must not invent or copy an unverified checksum.

## Required final metadata before submission

Record these fields once the exact packaged SBML file is available:

- Retrieval date and time in UTC.
- Exact URL or manual source used to obtain the SBML.
- BioModels accession and title.
- License statement and where it was observed.
- SBML level/version if available.
- SHA-256 checksum of the exact packaged XML file.
- Any BioModels page build or version string visible at retrieval time.
- Any access failures or fallback steps used.

## Download fallback endpoints to try

Try these with a normal user agent and record status codes:

1. `https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000151.3?filename=BIOMD0000000151_url.xml`
2. `https://www.biomodels.org/model/download/BIOMD0000000151.3?filename=BIOMD0000000151_url.xml`
3. `https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000151?filename=BIOMD0000000151_url.xml`
4. `https://www.biomodels.org/model/download/BIOMD0000000151?filename=BIOMD0000000151_url.xml`
5. `https://www.ebi.ac.uk/biomodels/BIOMD0000000151/download?filename=BIOMD0000000151_url.xml`
6. `https://www.ebi.ac.uk/biomodels/model/files/BIOMD0000000151/BIOMD0000000151_url.xml`
7. `https://www.ebi.ac.uk/biomodels/model/files/BIOMD0000000151/BIOMD0000000151.xml`

If all automated endpoints fail, use the BioModels web UI manually, save the SBML as `source/BIOMD0000000151.xml`, then run `python scripts/checksum.py source/BIOMD0000000151.xml > source/BIOMD0000000151.sha256` from this folder.
