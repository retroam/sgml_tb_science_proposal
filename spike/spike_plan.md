# SBML-backed feasibility spike plan

## Goal

Determine whether `BIOMD0000000151` can support a fair TB-Science task where an agent calibrates a reduced Netflux-style IL-6 model against SBML-derived public trajectories and predicts held-out perturbations.

## Inputs

- Source SBML: `../source/BIOMD0000000151.xml`.
- Checksum: `../source/BIOMD0000000151.sha256` generated from the exact XML.
- Starter topology: `reduced_network.json`.
- Seed: `151` for all sampling and optimization.

## Steps

1. Fetch and verify the SBML.
   - Run `python ../scripts/fetch_biomodel.py` from the `proposal` folder, or download manually.
   - Confirm the file is XML/SBML-looking and compute SHA-256.
   - Record retrieval URL, date, license, and checksum in `SOURCE.md` or task metadata.
2. Establish an SBML reference runner.
   - Use a local SBML simulator suitable for deterministic ODE trajectories, such as tellurium/roadrunner, libSBML plus scipy integration, COPASI, or AMICI.
   - This simulator is for benchmark authoring only. The final contestant task must not allow SBML simulation during hidden prediction.
3. Generate reference trajectories.
   - Simulate baseline IL-6 stimulation and a small set of perturbations over a fixed time grid, for example 0 to 180 minutes with 1 to 5 minute spacing.
   - Save normalized observables for IL6R/JAK/STAT3/SOCS3-related species or proxies available in the SBML.
   - Split conditions into public calibration and hidden verifier sets before tuning task difficulty.
4. Implement the reduced Netflux-style simulator.
   - Use normalized Hill activation and inhibition, bounded edge weights, node decay/time constants, and optional basal activity within the bounds in `reduced_network.json`.
   - Keep all parameters bounded and deterministic.
5. Fit on public conditions only.
   - Fit parameters by least squares or robust loss over full trajectories and summary features.
   - Use multiple deterministic starts with seed `151`.
6. Evaluate on held-out conditions.
   - Score trajectory RMSE, endpoint RMSE, peak timing error, and qualitative direction of perturbation response.
   - Compare against baselines listed below.
7. Decide feasibility.
   - Keep the task only if the reduced model beats simple baselines and hidden-condition performance is stable across reasonable public splits.

## Baselines

- Constant baseline: predict the public baseline trajectory for every condition.
- Endpoint baseline: linearly interpolate from initial value to public endpoint for each observable.
- No-calibration baseline: use midpoint parameters from `reduced_network.json`.
- Optional ablation: topology without SOCS3 feedback.

## Metrics

- Public fit trajectory RMSE by observable.
- Hidden trajectory RMSE by observable.
- Endpoint RMSE at final time.
- Peak time absolute error for STAT3-like observable.
- Perturbation direction accuracy relative to baseline, especially IL6 removal, JAK inhibition, STAT3 knockdown, and SOCS3 perturbation.

## Stop conditions

Stop and revise the proposal if any condition holds:

- The SBML cannot be obtained with clear redistribution rights.
- The SBML cannot be simulated deterministically in the authoring environment.
- No clear mapping exists from SBML species to the reduced observables.
- The five-node reduced model cannot beat the constant baseline on held-out perturbations.
- Calibration requires excessive runtime for the intended contestant limit.
- Hidden scoring is dominated by numerical instability rather than modeling quality.

## Expected spike outputs

- Verified SBML file and `.sha256` file under `../source/`.
- Public and hidden condition definitions.
- Public and hidden reference trajectories.
- A fitted parameter JSON from the reduced simulator.
- A short feasibility note with metrics and a go/no-go recommendation.
