# Helper scripts

Run these from the `proposal` folder.

- `python scripts/fetch_biomodel.py`: try likely BioModels SBML download endpoints for `BIOMD0000000151` and save the first SBML-looking response to `source/BIOMD0000000151.xml`.
- `python scripts/checksum.py source/BIOMD0000000151.xml`: print the SHA-256 checksum for the exact file.

Both scripts use only the Python standard library.
