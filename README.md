# SBML-to-Netflux calibration proposal handoff

This folder is the handoff package for the SBML-to-Netflux calibration task proposal. It is intended to be given to the next Amp orb as `@proposal`.

## Primary file

- `proposal.md`: the single active proposal text, copied from `tb_science/sbml-to-netflux-calibration-proposal.md`.

## Next-orb task summary

The next orb should run the real feasibility spike against the BioModels SBML source model `BIOMD0000000151` (`Singh2006_IL6_Signal_Transduction`). The main unresolved item is reliable SBML access. Use the helper script in `scripts/fetch_biomodel.py`, or manually download the SBML from BioModels, then save it as `source/BIOMD0000000151.xml`.

After the SBML is available, compute and record its SHA-256 checksum, generate deterministic SBML reference trajectories, implement the reduced Netflux-style simulator, fit the starter reduced network, and decide whether the task is feasible under the proposed runtime and grading constraints.

Do not invent checksums or license metadata. If BioModels remains unavailable, document exact endpoints tried, status codes, dates, and the manual fallback needed.

## Folder map

- `SOURCE.md`: source model metadata, access notes, and required final provenance fields.
- `source/`: put the fetched SBML XML and checksum here.
- `spike/spike_plan.md`: concrete feasibility spike plan.
- `spike/reduced_network.json`: five-node IL-6 starter topology for the spike.
- `scripts/checksum.py`: SHA-256 helper.
- `scripts/fetch_biomodel.py`: stdlib-only BioModels fetch helper.
- `writing_style_guide.md`: copied writing guidance, if present in the parent workspace.
