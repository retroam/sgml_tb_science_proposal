# SBML-to-Netflux: Reduced Signaling Model Calibration

## Scientific domain

**Domain:** Life Sciences  
**Field:** Biology / Computational Biology  
**Subfield:** Systems Biology / Signaling Models

## Proposed task slug

`sbml-netflux-calibration`

## Short summary

This task tests whether an AI agent can convert a conventional SBML signaling model into a calibrated Netflux-style normalized-Hill model. Given a permissively licensed BioModels SBML file, a fixed reduced signed network, public reference simulations, and a scaffolded Python pipeline, the agent implements the reduced model, calibrates its parameters, and predicts hidden SBML-derived perturbation responses.

The task does not ask the agent to read papers, infer network structure from prose, or digitize figures. The source SBML model is the reference system. The reduced Netflux-style model is judged by how well it preserves reference behavior under held-out perturbations.

## Candidate source model

The initial candidate is the Singh2006 IL-6 signal transduction model from BioModels:

- BioModels accession: `BIOMD0000000151`
- Source: <https://www.ebi.ac.uk/biomodels/BIOMD0000000151>
- Domain: mammalian cytokine signaling
- License prerequisite: verify the entry-specific BioModels license and redistribution metadata before submission. BioModels models are generally distributed under CC0, but the final task should cite the entry metadata, retrieval date, checksum, and license statement.

If this entry fails the license or solvability checks, use another curated, permissively licensed BioModels signaling model with comparable size and monotonic or weakly transient dynamics. Strong alternates include MAPK or EGF/EGFR BioModels entries, provided the packaged SBML source is the BioModels CC0 version.

## Problem statement

Systems biologists often reduce detailed mechanistic ODE models into smaller regulatory models that are easier to inspect, perturb, and reuse. This reduction is not a file-format conversion. The reduced model must preserve the behavior that matters for the scientific question while using simpler causal rules and fewer parameters.

The proposed TB-Science task asks the agent to complete a scaffolded Python pipeline that fits a Netflux-style normalized-Hill model to deterministic reference behavior from a provided SBML signaling model. The benchmark authors provide the reduced network topology so the task stays well-specified. The agent implements the model equations, calibrates bounded parameters, simulates public and hidden perturbations, and writes prediction files with normalized trajectories and summary features.

## Task objective

Complete the provided pipeline so it runs as:

```bash
python /root/run_pipeline.py \
  --network /root/data/derived_network.json \
  --public-conditions /root/data/public_conditions.json \
  --public-reference /root/data/public_reference_trajectories.csv \
  --hidden-conditions /root/data/conditions.json \
  --out /root/results/predictions.csv \
  --params-out /root/results/calibrated_parameters.json
```

The submitted implementation must:

1. load the fixed reduced network;
2. implement the public Netflux-style normalized-Hill equations;
3. calibrate allowed parameters against public SBML-derived reference trajectories;
4. simulate hidden perturbation conditions without calling the source SBML simulator;
5. write normalized trajectory predictions and calibrated parameters;
6. produce deterministic outputs under a fixed seed and runtime limit.

## Inputs provided to the agent

The agent-facing environment contains:

```text
/root/data/
  source_model.xml
  derived_network.json
  species_mapping.json
  public_conditions.json
  public_reference_trajectories.csv
  evaluation_spec.md
/root/run_pipeline.py
/root/src/
```

### `source_model.xml`

The exact SBML source model used to generate public references. The source model is included for scientific context and local inspection. The hidden verifier should reject solutions that replay the SBML model instead of running the specified reduced Netflux-style model.

### `derived_network.json`

The fixed reduced network. It defines nodes, signed edges, inputs, observables, parameter bounds, initial states, and allowed perturbation targets.

Example shape:

```json
{
  "nodes": ["IL6", "IL6R", "JAK", "STAT3", "SOCS3"],
  "edges": [
    {"source": "IL6", "target": "IL6R", "sign": "activation"},
    {"source": "IL6R", "target": "JAK", "sign": "activation"},
    {"source": "JAK", "target": "STAT3", "sign": "activation"},
    {"source": "STAT3", "target": "SOCS3", "sign": "activation"},
    {"source": "SOCS3", "target": "JAK", "sign": "inhibition"}
  ],
  "observables": {
    "STAT3_active": ["SBML_SPECIES_ID_1"],
    "SOCS3": ["SBML_SPECIES_ID_2"]
  },
  "parameter_bounds": {
    "weight": [0.0, 2.0],
    "ec50": [0.01, 1.0],
    "hill": [1.0, 4.0],
    "tau": [0.1, 100.0],
    "basal": [0.0, 1.0]
  }
}
```

The topology is not graded as an inference problem. Agents may calibrate allowed parameters, but they may not add nodes, delete nodes, add edges, delete edges, or change observable mappings.

### `public_conditions.json`

Public training conditions. Conditions may include ligand dose changes, initial-state changes, single-node inhibition, or bounded perturbations that map cleanly to the reduced network.

### `public_reference_trajectories.csv`

Reference trajectories generated by deterministic simulation of the SBML source model under public conditions. These are training targets, not hidden answers.

## Model specification

The reduced model uses bounded node activities `x_i(t) in [0, 1]`.

For an activating edge from source `j` to target `i`:

```text
act_j = weight * x_j^hill / (ec50^hill + x_j^hill)
```

For an inhibitory edge:

```text
inh_j = weight * ec50^hill / (ec50^hill + x_j^hill)
```

The final task must define one exact multi-input rule before release. A simple candidate is weighted continuous OR for regulators with the same sign and multiplication for explicitly grouped AND rules. The rule must be public, deterministic, and shared by public and hidden tests.

Each node follows:

```text
dx_i/dt = (basal_i + F_i(x) - x_i) / tau_i
```

with clipping to `[0, 1]` after each solver step. The task should use one public solver policy, such as `solve_ivp` with fixed tolerances or a fixed-step explicit integrator with stated `dt`, horizon, convergence criterion, and random seed. Solver choice must be locked before submission and validated on the chosen source model.

## Outputs

### `calibrated_parameters.json`

The calibrated reduced-model parameters. The file must contain only allowed parameters and must respect all public bounds.

### `predictions.csv`

One row per hidden condition, observable, and time point:

```csv
condition_id,observable,time,predicted_value
baseline,STAT3_active,0.000,0.00000000
baseline,STAT3_active,5.000,0.18230000
baseline,SOCS3,5.000,0.04120000
```

Values are normalized floats in `[0, 1]` with at least eight digits after the decimal point.

### `summary.csv`

One row per hidden condition and observable:

```csv
condition_id,observable,final_value,peak_value,time_to_peak,auc,direction
baseline,STAT3_active,0.52000000,0.83000000,20.000,18.24000000,up
```

Allowed directions are `up`, `down`, and `unchanged`, computed from public thresholds in `evaluation_spec.md`.

## Verification plan

The task should use TB-Science separate verifier mode. The verifier contains hidden conditions, hidden SBML-derived reference outputs, and scoring code. It copies submitted artifacts into a clean environment, runs the submitted reduced-model simulator on hidden conditions, and compares outputs to the reference.

The verifier must not trust public predictions generated during the agent run. It should rerun the submitted code with verifier-only condition files.

### Declared artifacts

The implementation should declare artifacts such as:

```toml
artifacts = [
  "/root/results/predictions.csv",
  "/root/results/summary.csv",
  "/root/results/calibrated_parameters.json",
  "/root/run_pipeline.py",
  "/root/src"
]
```

Exact artifact paths should match the final Harbor task template.

### Reference generation

Benchmark authors generate reference data by simulating the source SBML model under public and hidden conditions with a pinned toolchain, such as libRoadRunner, AMICI, COPASI, or Tellurium. The task should record the simulator version, solver settings, time grid, normalization rule, and checksums for every reference file.

The verifier compares against these generated references, not digitized figures from papers.

### Metrics

Primary metric:

```text
mean absolute normalized trajectory error across hidden conditions, observables, and time points
```

Secondary metrics:

- final-state error;
- area-under-curve error;
- peak-value error;
- time-to-peak error, if the selected model has robust peaks;
- perturbation direction accuracy.

The pass threshold should be calibrated with baseline submissions:

1. constant predictor;
2. uncalibrated default Netflux model;
3. random-search calibration;
4. optimizer-based calibration;
5. benchmark-author reference solution.

Direction-only solutions should not pass. Public thresholds should be loose enough for a valid reduced model and tight enough to reject constant, default, and overfit solutions.

## Hidden tests

Hidden tests should include:

1. **Held-out perturbations**
   - ligand doses not present in public training data;
   - single-node inhibition or knockdown conditions;
   - combined perturbations;
   - alternative simulation horizons or sampling grids.

2. **Generalization checks**
   - hidden conditions that test feedback behavior;
   - perturbations of upstream and downstream nodes;
   - conditions where public-trajectory interpolation is insufficient.

3. **Metamorphic checks**
   - row order in condition files does not change predictions;
   - repeated runs are deterministic;
   - irrelevant condition metadata does not affect outputs;
   - parameter files outside allowed bounds fail validation.

4. **Anti-cheat checks**
   - network access disabled;
   - direct calls to SBML simulation packages disallowed during hidden evaluation;
   - submitted code must operate through the reduced-model interface;
   - cached public outputs do not help on verifier-only conditions.

## Why this is verifiable

The task has concrete outputs: calibrated parameters, normalized trajectories, and summary features. A deterministic SBML reference pipeline generates hidden targets. The verifier checks numeric agreement, schema validity, parameter bounds, deterministic behavior, and runtime.

No human judge decides whether a model "looks right." The scoring metric and normalization rule are public.

## Why this is well-specified

The task provides the source SBML file, fixed reduced topology, observable mapping, allowed parameters, parameter bounds, perturbation schema, solver policy, normalization rule, output schema, and scoring metric.

The agent does not infer network structure from papers. The agent solves a constrained model-reduction and calibration problem.

## Why this is solvable

An expert can solve the task by implementing the public normalized-Hill model, choosing a bounded optimizer, fitting to public trajectories, validating on held-out public splits, and writing the required output files. The task uses standard scientific Python tools and local data.

Before submission, the benchmark authors should run a feasibility spike on the chosen BioModels entry. The spike must show that a reduced normalized-Hill model can match held-out SBML-derived behavior within a discriminative tolerance.

## Why this is difficult

The task asks for a useful reduced model, not a direct replay of the source simulator. The agent must balance nonlinear parameter fitting, bounded ODE simulation, normalization, feedback behavior, and hidden-condition generalization.

Poor solutions can fit public trajectories while failing hidden doses or perturbations. Direction-only heuristics, constant predictors, and uncalibrated defaults should fail.

## Why this is scientifically grounded

Reducing detailed mechanistic ODE models into smaller regulatory models is a real systems-biology workflow. Scientists use reduced models to inspect pathway logic, test perturbations, and communicate mechanisms when detailed kinetic models are too large or too parameter-heavy for the question at hand.

The task uses a published, curated SBML signaling model as the source system and tests whether the reduced model preserves specified behaviors under perturbation.

## Why this is outcome-verified

The verifier grades only submitted artifacts and simulated outputs. It does not require a particular optimizer, coding style, or calibration procedure. Agents may use any method that produces a valid reduced model within the runtime limit.

## Safety and reproducibility

The task uses a published computational signaling model and simulated perturbations only. It does not involve wet-lab protocols, pathogen engineering, clinical recommendations, patient data, or live biological database access.

The source SBML file, derived network, public references, solver versions, and reference-generation scripts should be pinned and checksummed. Hidden references should be generated from the same pipeline.

## Proposal-form text

**Task title:** SBML-to-Netflux: Reduced Signaling Model Calibration

**Scientific domain:** Life Sciences / Biology / Systems Biology

**Short description:** Calibrate a Netflux-style normalized-Hill signaling model so it preserves behavior from a provided SBML ODE model under hidden perturbations.

**Task description:** Given a permissively licensed SBML signaling model, a fixed reduced signed network, public SBML-derived reference trajectories, and a scaffolded Python interface, the agent must implement a Netflux-style normalized-Hill simulator, calibrate bounded parameters, and predict normalized trajectories for hidden perturbation conditions. The verifier compares the submitted reduced-model outputs against deterministic references generated from the source SBML model.

**Why it is scientifically meaningful:** Scientists often reduce detailed mechanistic ODE models into smaller regulatory models that preserve key perturbation behavior. This task evaluates whether an agent can perform that model-reduction and calibration workflow reproducibly.

**Why it is difficult:** The task combines nonlinear parameter calibration, bounded ODE simulation, trajectory normalization, feedback behavior, and hidden-condition generalization. Public training traces are insufficient for hardcoding because hidden perturbations come from the SBML reference model.

**How it is verified:** The verifier reruns the submitted reduced-model simulator on hidden perturbation conditions in a separate environment and compares normalized trajectories and summary features to deterministic SBML-derived references. It checks file schemas, parameter bounds, numerical error, direction labels, deterministic repeated runs, and runtime.

**Why it is safe and reproducible:** The task uses local files, a permissively licensed computational model, deterministic simulation references, pinned solver settings, and no network access during verification. It performs only in silico perturbations.

**Expected expert time:** 4-8 hours for a computational systems biologist or scientific Python developer familiar with ODE models and parameter fitting.

## Pre-submission checklist

- Verify the chosen BioModels entry license and redistribution metadata.
- Pin the exact SBML file, retrieval date, and checksum.
- Run a feasibility spike showing the reduced model can match held-out SBML behavior with a useful tolerance.
- Freeze the derived network topology and observable mapping.
- Choose the exact solver policy for reduced-model simulation.
- Generate public and hidden reference trajectories from the same SBML pipeline.
- Calibrate pass thresholds against baseline submissions.
- Confirm Harbor artifact paths and verifier invocation.
