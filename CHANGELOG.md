# Changelog

## [7.0.1](https://github.com/Flagsmith/flagsmith-engine/compare/v7.0.0...v7.0.1) (2025-09-11)

### Bug Fixes

- Incorrect `TARGETING_MATCH` reasons ([#258](https://github.com/Flagsmith/flagsmith-engine/issues/258))
  ([3f12e5f](https://github.com/Flagsmith/flagsmith-engine/commit/3f12e5faa67636af7f7016eec673088959f8017b))
- PERCENTAGE_SPLIT working for undefined keys ([#256](https://github.com/Flagsmith/flagsmith-engine/issues/256))
  ([fa37c6c](https://github.com/Flagsmith/flagsmith-engine/commit/fa37c6ca52632030ea307347cf529c774ef6d198))

## [7.0.0](https://github.com/Flagsmith/flagsmith-engine/compare/v6.1.0...v7.0.0) (2025-09-01)

### ⚠ BREAKING CHANGES

- **v7:** Remove deprecated APIs, Pydantic models ([#250](https://github.com/Flagsmith/flagsmith-engine/issues/250))
- Drop Python 3.8 support ([#249](https://github.com/Flagsmith/flagsmith-engine/issues/249))

### Features

- Add Codspeed benchmark ([#244](https://github.com/Flagsmith/flagsmith-engine/issues/244))
  ([622b372](https://github.com/Flagsmith/flagsmith-engine/commit/622b372f32cd0ba6bd875493b13969a1cf0dcf67))
- Drop Python 3.8 support ([#249](https://github.com/Flagsmith/flagsmith-engine/issues/249))
  ([63b546c](https://github.com/Flagsmith/flagsmith-engine/commit/63b546c0faa48c4dcae0156595183590445129dc))
- Support returning default flags for `None` identities
  ([#254](https://github.com/Flagsmith/flagsmith-engine/issues/254))
  ([a05befa](https://github.com/Flagsmith/flagsmith-engine/commit/a05befaea7b1db8178a37fbb10d3a0d581443609))
- **v7:** JSONPath support ([#243](https://github.com/Flagsmith/flagsmith-engine/issues/243))
  ([5b0136f](https://github.com/Flagsmith/flagsmith-engine/commit/5b0136fda496680ae80a74e627726de676db9a05))
- **v7:** Remove deprecated APIs, Pydantic models ([#250](https://github.com/Flagsmith/flagsmith-engine/issues/250))
  ([92de872](https://github.com/Flagsmith/flagsmith-engine/commit/92de8726af9f33d8f27b75b2743093234f773080))
- **v7:** Support `string[]` as condition value for the `IN` operator
  ([#255](https://github.com/Flagsmith/flagsmith-engine/issues/255))
  ([68d49d0](https://github.com/Flagsmith/flagsmith-engine/commit/68d49d0b0cf19a01e3659668b1dda5178987a491))

### CI

- Exclude coverage from benchmark ([#248](https://github.com/Flagsmith/flagsmith-engine/issues/248))
  ([770680b](https://github.com/Flagsmith/flagsmith-engine/commit/770680b600fd1d3094d372b47ec22993e1a66597))
- Run tests and benchmarks on main ([#247](https://github.com/Flagsmith/flagsmith-engine/issues/247))
  ([5376cb9](https://github.com/Flagsmith/flagsmith-engine/commit/5376cb903fc4488bf31b4899df65549a3f48d75c))

### Other

- add root CODEOWNERS ([#253](https://github.com/Flagsmith/flagsmith-engine/issues/253))
  ([f99fa99](https://github.com/Flagsmith/flagsmith-engine/commit/f99fa99c8a67dafff1b3373006c5eac835def226))

## [6.1.0](https://github.com/Flagsmith/flagsmith-engine/compare/v6.0.2...v6.1.0) (2025-08-18)

### Features

- **v7:** `get_evaluation_result` ([#239](https://github.com/Flagsmith/flagsmith-engine/issues/239))
  ([b1e4447](https://github.com/Flagsmith/flagsmith-engine/commit/b1e444733c14e74a61cac9b1173518366e34b31a))

### Other

- Drop Python 3.7 support ([#240](https://github.com/Flagsmith/flagsmith-engine/issues/240))
  ([ffadc79](https://github.com/Flagsmith/flagsmith-engine/commit/ffadc79fffe0328e77360d609fea159fef7befaf))

## [6.0.2](https://github.com/Flagsmith/flagsmith-engine/compare/v6.0.1...v6.0.2) (2025-08-06)

### Bug Fixes

- reintroduced-get-identity-segments ([#237](https://github.com/Flagsmith/flagsmith-engine/issues/237))
  ([efe710c](https://github.com/Flagsmith/flagsmith-engine/commit/efe710ce456064f7e01934f18f4773e24ae3d266))

## [6.0.1](https://github.com/Flagsmith/flagsmith-engine/compare/v6.0.0...v6.0.1) (2025-08-06)

### Bug Fixes

- added-none-check-in-context-matches-condition ([#236](https://github.com/Flagsmith/flagsmith-engine/issues/236))
  ([fc5bf44](https://github.com/Flagsmith/flagsmith-engine/commit/fc5bf448d780acd78b614996151252eef59864a3))

### CI

- Publish a wheel, move on from deprecated `setup.py` usage
  ([#230](https://github.com/Flagsmith/flagsmith-engine/issues/230))
  ([f43dcc8](https://github.com/Flagsmith/flagsmith-engine/commit/f43dcc83d60b6f5ad478e6382ba451d29c441474))

## [6.0.0](https://github.com/Flagsmith/flagsmith-engine/compare/v5.4.1...v6.0.0) (2025-07-21)

### ⚠ BREAKING CHANGES

- Release latest changes as breaking ([#227](https://github.com/Flagsmith/flagsmith-engine/issues/227))

### Features

- Release latest changes as breaking ([#227](https://github.com/Flagsmith/flagsmith-engine/issues/227))
  ([a6d42b2](https://github.com/Flagsmith/flagsmith-engine/commit/a6d42b2b625dd6a3278daabb05fabcd4850a02ae))

## [5.4.1](https://github.com/Flagsmith/flagsmith-engine/compare/v5.4.0...v5.4.1) (2025-07-21)

### Bug Fixes

- `ImportError` when trying to import the `TraitValue` type
  ([#224](https://github.com/Flagsmith/flagsmith-engine/issues/224))
  ([6133b96](https://github.com/Flagsmith/flagsmith-engine/commit/6133b96921a21c195f7ee7eb1c09004ed87de81f))

## [5.4.0](https://github.com/Flagsmith/flagsmith-engine/compare/v5.3.1...v5.4.0) (2025-07-21)

### Features

- Context values for Segments ([#220](https://github.com/Flagsmith/flagsmith-engine/issues/220))
  ([01e7a56](https://github.com/Flagsmith/flagsmith-engine/commit/01e7a56ad040aaf17ddc6e1ccc3c0bf9b5f24864))

## [5.3.1](https://github.com/Flagsmith/flagsmith-engine/compare/v5.3.0...v5.3.1) (2025-06-30)

### CI

- add release please ([#214](https://github.com/Flagsmith/flagsmith-engine/issues/214))
  ([6ff5a0a](https://github.com/Flagsmith/flagsmith-engine/commit/6ff5a0a3ccda254943426c732912dfa29661b88a))

### Other

- add sane model defaults to OrganisationModel and ProjectModel
  ([#213](https://github.com/Flagsmith/flagsmith-engine/issues/213))
  ([d909c2f](https://github.com/Flagsmith/flagsmith-engine/commit/d909c2f040512cecd88fb629405673daccc6d1d7))
- **deps:** bump pydantic from 2.3.0 to 2.4.0 ([#206](https://github.com/Flagsmith/flagsmith-engine/issues/206))
  ([eb02943](https://github.com/Flagsmith/flagsmith-engine/commit/eb029439dde033fe5c03cb567393d3d8b36446d9))

<a id="v5.3.0"></a>

## [v5.3.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v5.3.0) - 2024-09-24

## What's Changed

- feat: make map_any_value_to_trait_value public to allow trait value parsing in core by
  [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#211](https://github.com/Flagsmith/flagsmith-engine/pull/211)
- chore: bump minor version by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#212](https://github.com/Flagsmith/flagsmith-engine/pull/212)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v5.2.0...v5.3.0

[Changes][v5.3.0]

<a id="v5.2.0"></a>

## [v5.2.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v5.2.0) - 2024-09-04

## What's Changed

- chore(deps-dev): bump black from 23.7.0 to 24.3.0 by [@dependabot](https://github.com/dependabot) in
  [Flagsmith/flagsmith-engine#203](https://github.com/Flagsmith/flagsmith-engine/pull/203)
- chore: update github actions by [@dabeeeenster](https://github.com/dabeeeenster) in
  [Flagsmith/flagsmith-engine#204](https://github.com/Flagsmith/flagsmith-engine/pull/204)
- feat(env/model): Add use_identity_overrides_in_local_eval field by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#208](https://github.com/Flagsmith/flagsmith-engine/pull/208)
- feat(env/model): add dashboard_alias field by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#210](https://github.com/Flagsmith/flagsmith-engine/pull/210)
- chore: bump version by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#209](https://github.com/Flagsmith/flagsmith-engine/pull/209)

## New Contributors

- [@dependabot](https://github.com/dependabot) made their first contribution in
  [Flagsmith/flagsmith-engine#203](https://github.com/Flagsmith/flagsmith-engine/pull/203)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v5.1.1...v5.2.0

[Changes][v5.2.0]

<a id="v5.1.1"></a>

## [Version 5.1.1 (v5.1.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v5.1.1) - 2024-01-17

## What's Changed

- fix: Avoid recursion during identity features validation by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#201](https://github.com/Flagsmith/flagsmith-engine/pull/201)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v5.1.0...v5.1.1

[Changes][v5.1.1]

<a id="v5.1.0"></a>

## [Version 5.1.0 (v5.1.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v5.1.0) - 2023-12-15

## What's Changed

- feat: remove builders modules by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#195](https://github.com/Flagsmith/flagsmith-engine/pull/195)
- feat: Add `EnvironmentModel.identity_overrides` for the local evaluation mode by [@khvn26](https://github.com/khvn26)
  in [Flagsmith/flagsmith-engine#199](https://github.com/Flagsmith/flagsmith-engine/pull/199)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v5.0.0...v5.1.0

[Changes][v5.1.0]

<a id="v5.0.0"></a>

## [Version 5.0.0 (v5.0.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v5.0.0) - 2023-11-08

## What's Changed

- feat: pydantic V2 by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#190](https://github.com/Flagsmith/flagsmith-engine/pull/190)
- feat: strict typing by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#168](https://github.com/Flagsmith/flagsmith-engine/pull/168)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v4.1.0...v5.0.0

[Changes][v5.0.0]

<a id="v4.1.0"></a>

## [Version 4.1.0 (v4.1.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v4.1.0) - 2023-09-19

## What's Changed

- feat: evaluator module by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#192](https://github.com/Flagsmith/flagsmith-engine/pull/192)
- ci/bump pytest by [@dabeeeenster](https://github.com/dabeeeenster) in
  [Flagsmith/flagsmith-engine#191](https://github.com/Flagsmith/flagsmith-engine/pull/191)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v4.0.4...v4.1.0

[Changes][v4.1.0]

<a id="v4.0.4"></a>

## [Version 4.0.4 (v4.0.4)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v4.0.4) - 2023-08-08

## What's Changed

- fix: decimal trait values by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#187](https://github.com/Flagsmith/flagsmith-engine/pull/187)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v4.0.3...v4.0.4

[Changes][v4.0.4]

<a id="v4.0.3"></a>

## [Version 4.0.3 (v4.0.3)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v4.0.3) - 2023-07-12

## What's Changed

- Fix Nan validation by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#184](https://github.com/Flagsmith/flagsmith-engine/pull/184)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v4.0.2...v4.0.3

[Changes][v4.0.3]

<a id="v4.0.2"></a>

## [Version 4.0.2 (v4.0.2)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v4.0.2) - 2023-07-04

## What's Changed

- fix: restore trait value coercion to string by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#179](https://github.com/Flagsmith/flagsmith-engine/pull/179)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v4.0.1...v4.0.2

[Changes][v4.0.2]

<a id="v4.0.1"></a>

## [Version 4.0.1 (v4.0.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v4.0.1) - 2023-07-03

## What's Changed

- fix: use `Config.smart_union` to avoid type coercion for `TraitModel.trait_value` by
  [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#177](https://github.com/Flagsmith/flagsmith-engine/pull/177)
- fix: remove dynatrace from engine integration models by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#176](https://github.com/Flagsmith/flagsmith-engine/pull/176)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v4.0.0...v4.0.1

[Changes][v4.0.1]

<a id="v4.0.0"></a>

## [Version 4.0.0 (v4.0.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v4.0.0) - 2023-06-29

## What's Changed

Support for Python versions earlier than 3.7 is dropped.

This release removes the functionality that supported Flagsmith's Core API <> Edge API interop and migrates the engine
model dataclasses to Pydantic, simplifying their serialization.

`flag_engine.environments.builders` and `flag_engine.identities.builders` modules are kept for backwards compatibility
but will be deprecated in the future in favour of Pydantic's `.dict()` and `.parse_obj()` methods. It's completely safe
to use them with Flagsmith's `EnvironmentModel` and `IdentityModel` instead of builder APIs.

- feat: migrate from marshmallow to pydantic, remove core API-specific schemas by [@khvn26](https://github.com/khvn26)
  in [Flagsmith/flagsmith-engine#167](https://github.com/Flagsmith/flagsmith-engine/pull/167)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.6.0...v4.0.0

[Changes][v4.0.0]

<a id="v3.6.0"></a>

## [Version 3.6.0 (v3.6.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.6.0) - 2023-06-29

## What's Changed

- Ensure percentage split evaluations are consistent in Core API and Local Evaluation by
  [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#171](https://github.com/Flagsmith/flagsmith-engine/pull/171)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.5.1...v3.6.0

[Changes][v3.6.0]

<a id="v3.5.1"></a>

## [v3.5.1](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.5.1) - 2023-06-26

## What's Changed

- feat: add Rudderstack support by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#169](https://github.com/Flagsmith/flagsmith-engine/pull/169)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.5.0...v3.5.1

[Changes][v3.5.1]

<a id="v3.5.0"></a>

## [v3.5.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.5.0) - 2023-05-19

## What's Changed

- feat: add `Project.server_key_only_feature_ids` by [@khvn26](https://github.com/khvn26) in
  [Flagsmith/flagsmith-engine#164](https://github.com/Flagsmith/flagsmith-engine/pull/164)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.4.0...v3.5.0

[Changes][v3.5.0]

<a id="v3.4.0"></a>

## [v3.4.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.4.0) - 2023-04-11

## What's Changed

- feat(environment): Add hide_sensitive_data field by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#161](https://github.com/Flagsmith/flagsmith-engine/pull/161)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.3.2...v3.4.0

[Changes][v3.4.0]

<a id="v3.3.2"></a>

## [Version 3.3.2 (v3.3.2)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.3.2) - 2023-03-29

## What's Changed

- Update feature state version logic by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#159](https://github.com/Flagsmith/flagsmith-engine/pull/159)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.3.1...v3.3.2

[Changes][v3.3.2]

<a id="v3.3.1"></a>

## [Version 3.3.1 (v3.3.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.3.1) - 2023-03-16

## What's Changed

- Fix regex evaluations for non string trait values by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#157](https://github.com/Flagsmith/flagsmith-engine/pull/157)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.3.0...v3.3.1

[Changes][v3.3.1]

<a id="v3.3.0"></a>

## [v3.3.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.3.0) - 2023-03-03

## What's Changed

- feat(environment): Add name by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#154](https://github.com/Flagsmith/flagsmith-engine/pull/154)
- Release 3.3.0 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#155](https://github.com/Flagsmith/flagsmith-engine/pull/155)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/3.2.0...v3.3.0

[Changes][v3.3.0]

<a id="3.2.0"></a>

## [3.2.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/3.2.0) - 2023-02-02

## What's Changed

- Feat(identity/get_hash_key): Add method to help generate consistent mv values by
  [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#152](https://github.com/Flagsmith/flagsmith-engine/pull/152)
- Release 3.2.0 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#153](https://github.com/Flagsmith/flagsmith-engine/pull/153)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.1.0...3.2.0

[Changes][3.2.0]

<a id="v3.1.0"></a>

## [v3.1.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.1.0) - 2023-01-16

## What's Changed

- In segment operator added by [@EdsnLoor](https://github.com/EdsnLoor) in
  [Flagsmith/flagsmith-engine#149](https://github.com/Flagsmith/flagsmith-engine/pull/149)
- feat(env/hide_disabled_flags): Add hide_disabled flags to environment by
  [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#150](https://github.com/Flagsmith/flagsmith-engine/pull/150)

## New Contributors

- [@EdsnLoor](https://github.com/EdsnLoor) made their first contribution in
  [Flagsmith/flagsmith-engine#149](https://github.com/Flagsmith/flagsmith-engine/pull/149)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v3.0.0...v3.1.0

[Changes][v3.1.0]

<a id="v3.0.0"></a>

## [v3.0.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v3.0.0) - 2022-11-11

## What's Changed

- feat(identity/update_traits): update return type by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#146](https://github.com/Flagsmith/flagsmith-engine/pull/146)
- feat(project/models): Add enable_realtime_updates field by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#147](https://github.com/Flagsmith/flagsmith-engine/pull/147)
- feat(enviroment): add updated_at field by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#148](https://github.com/Flagsmith/flagsmith-engine/pull/148)
- Release 3.0.0 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#116](https://github.com/Flagsmith/flagsmith-engine/pull/116)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.3.0...v3.0.0

[Changes][v3.0.0]

<a id="v2.3.0"></a>

## [v2.3.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.3.0) - 2022-10-13

## What's Changed

- feat(modulo): Add support for modulo operator by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#144](https://github.com/Flagsmith/flagsmith-engine/pull/144)
- feat(segment): Add IS_SET and IS_NOT_SET operator by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#145](https://github.com/Flagsmith/flagsmith-engine/pull/145)
- Release v2.3.0 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#143](https://github.com/Flagsmith/flagsmith-engine/pull/143)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.2.0...v2.3.0

[Changes][v2.3.0]

<a id="v2.2.0"></a>

## [v2.2.0](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.2.0) - 2022-09-13

## What's Changed

- Release v2.2.0 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#142](https://github.com/Flagsmith/flagsmith-engine/pull/142)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.1.2...v2.2.0

[Changes][v2.2.0]

<a id="v2.1.2"></a>

## [v2.1.2](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.1.2) - 2022-09-13

## What's Changed

- Add pip-tools for managing dev requirements by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#138](https://github.com/Flagsmith/flagsmith-engine/pull/138)
- Update engine test data by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#140](https://github.com/Flagsmith/flagsmith-engine/pull/140)
- Release 2.1.2 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#139](https://github.com/Flagsmith/flagsmith-engine/pull/139)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.1.1...v2.1.2

[Changes][v2.1.2]

<a id="v2.1.1"></a>

## [Version 2.1.1 (v2.1.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.1.1) - 2022-07-01

## What's Changed

- Add allow_client_traits field to EnvironmentModel and schema by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#137](https://github.com/Flagsmith/flagsmith-engine/pull/137)
- Release 2.1.1 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#136](https://github.com/Flagsmith/flagsmith-engine/pull/136)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.1.0...v2.1.1

[Changes][v2.1.1]

<a id="v2.1.0"></a>

## [Version 2.1.0 (v2.1.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.1.0) - 2022-06-29

## What's Changed

- Replace environment webhooks with webhook config by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#134](https://github.com/Flagsmith/flagsmith-engine/pull/134)
- fix(ValueError/for-invalid-trait-value): catch and return False by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#132](https://github.com/Flagsmith/flagsmith-engine/pull/132)
- Release 2.1.0 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#135](https://github.com/Flagsmith/flagsmith-engine/pull/135)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.7...v2.1.0

[Changes][v2.1.0]

<a id="v2.0.7"></a>

## [Version 2.0.7 (v2.0.7)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.7) - 2022-05-27

## What's Changed

- Remove webhooks from \_INTEGRATION_ATTS by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#130](https://github.com/Flagsmith/flagsmith-engine/pull/130)
- Bump version 2.0.7 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#131](https://github.com/Flagsmith/flagsmith-engine/pull/131)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.6...v2.0.7

[Changes][v2.0.7]

<a id="v2.0.6"></a>

## [Version 2.0.6 (v2.0.6)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.6) - 2022-05-24

## What's Changed

- fix(segment-priority): use priority on evaluation by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#128](https://github.com/Flagsmith/flagsmith-engine/pull/128)
- Release 2.0.6 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#129](https://github.com/Flagsmith/flagsmith-engine/pull/129)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.5...v2.0.6

[Changes][v2.0.6]

<a id="v2.0.5"></a>

## [Version 2.0.5 (v2.0.5)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.5) - 2022-05-12

## What's Changed

- Return updated traits when updating by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#126](https://github.com/Flagsmith/flagsmith-engine/pull/126)
- Release 2.0.5 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#125](https://github.com/Flagsmith/flagsmith-engine/pull/125)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.4...v2.0.5

[Changes][v2.0.5]

<a id="v2.0.4"></a>

## [v2.0.4](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.4) - 2022-05-12

## What's Changed

- Add webhooks
- Add `entity_selector` to integration model/schema
- Release 2.0.4 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#122](https://github.com/Flagsmith/flagsmith-engine/pull/122)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.3...v2.0.4

[Changes][v2.0.4]

<a id="v2.0.3"></a>

## [v2.0.3](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.3) - 2022-05-09

## What's Changed

- Fix missing `feature_state_value` field on dump using engine models
- Release 2.0.3 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#120](https://github.com/Flagsmith/flagsmith-engine/pull/120)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.2...v2.0.3

[Changes][v2.0.3]

<a id="v2.0.2"></a>

## [v2.0.2](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.2) - 2022-04-25

## What's Changed

- fix(traits/float_value): Add custom field to serialize/deserialize trait_value
- Release 2.0.2 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#115](https://github.com/Flagsmith/flagsmith-engine/pull/115)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.1...v2.0.2

[Changes][v2.0.2]

<a id="v2.0.1"></a>

## [Version 2.0.1 (v2.0.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.1) - 2022-04-21

## What's Changed

- Add semver to install_requires by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#113](https://github.com/Flagsmith/flagsmith-engine/pull/113)
- Release 2.0.1 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#112](https://github.com/Flagsmith/flagsmith-engine/pull/112)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v2.0.0...v2.0.1

[Changes][v2.0.1]

<a id="v2.0.0-alpha.1"></a>

## [Version 2.0.0 - alpha 1 (v2.0.0-alpha.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.0-alpha.1) - 2022-04-21

[Changes][v2.0.0-alpha.1]

<a id="v2.0.0"></a>

## [Version 2.0.0 (v2.0.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v2.0.0) - 2022-04-21

## What's Changed

- Use feature state is_live by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#111](https://github.com/Flagsmith/flagsmith-engine/pull/111)
- major version update by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#108](https://github.com/Flagsmith/flagsmith-engine/pull/108)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.6...v2.0.0

[Changes][v2.0.0]

<a id="v1.6.6"></a>

## [Version 1.6.6 (v1.6.6)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.6) - 2022-04-21

## What's Changed

- Use timezone aware datetimes by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#110](https://github.com/Flagsmith/flagsmith-engine/pull/110)
- Release 1.6.6 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#109](https://github.com/Flagsmith/flagsmith-engine/pull/109)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.5...v1.6.6

[Changes][v1.6.6]

<a id="v1.6.5"></a>

## [Version 1.6.5 (v1.6.5)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.5) - 2022-04-20

## What's Changed

- Update comments by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#98](https://github.com/Flagsmith/flagsmith-engine/pull/98)
- Update engine test data by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#99](https://github.com/Flagsmith/flagsmith-engine/pull/99)
- fix(segment_evaluation): use django_id if present by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#101](https://github.com/Flagsmith/flagsmith-engine/pull/101)
- chore(tests): update engine test-data by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#105](https://github.com/Flagsmith/flagsmith-engine/pull/105)
- Handle feature state versioning by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#100](https://github.com/Flagsmith/flagsmith-engine/pull/100)
- Feature/edge api 29/add integrations data property by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#104](https://github.com/Flagsmith/flagsmith-engine/pull/104)
- fix(datetime): use tz(utc) aware datetime by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#103](https://github.com/Flagsmith/flagsmith-engine/pull/103)
- remove get_feature_state_value method by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#102](https://github.com/Flagsmith/flagsmith-engine/pull/102)
- Release 1.6.5 by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#97](https://github.com/Flagsmith/flagsmith-engine/pull/97)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.4...v1.6.5

[Changes][v1.6.5]

<a id="v1.6.4"></a>

## [v1.6.4](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.4) - 2022-02-10

## What's Changed

- Fix build_environment_api_key_model by adding correct parent class to schema by
  [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#95](https://github.com/Flagsmith/flagsmith-engine/pull/95)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.3...v1.6.4

[Changes][v1.6.4]

<a id="v1.6.3"></a>

## [v1.6.3](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.3) - 2022-02-04

## What's Changed

- Fix(feature/schema): only run validation if field the is present by [@gagantrivedi](https://github.com/gagantrivedi)
  in [Flagsmith/flagsmith-engine#94](https://github.com/Flagsmith/flagsmith-engine/pull/94)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.2...v1.6.3

[Changes][v1.6.3]

<a id="v1.6.2"></a>

## [Version 1.6.2 (v1.6.2)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.2) - 2022-02-03

## What's Changed

- Fix type error when sorting feature segments by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#91](https://github.com/Flagsmith/flagsmith-engine/pull/91)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.1...v1.6.2

[Changes][v1.6.2]

<a id="v1.6.1"></a>

## [Version 1.6.1 (v1.6.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.1) - 2022-02-02

## What's Changed

- Refactor django_transform module to allow for better query optimisation by
  [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#89](https://github.com/Flagsmith/flagsmith-engine/pull/89)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.6.0...v1.6.1

[Changes][v1.6.1]

<a id="v1.6.0"></a>

## [Version 1.6.0 (v1.6.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.6.0) - 2022-01-27

## What's Changed

- Feat(environment-api-key): Add environment api key model by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#86](https://github.com/Flagsmith/flagsmith-engine/pull/86)
- Update get_value typehints and add docstring by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#85](https://github.com/Flagsmith/flagsmith-engine/pull/85)
- Version bump (1.6.0) by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#88](https://github.com/Flagsmith/flagsmith-engine/pull/88)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.5.1...v1.6.0

[Changes][v1.6.0]

<a id="v1.5.1"></a>

## [Version 1.5.1 (v1.5.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.5.1) - 2022-01-07

## What's Changed

- fix(multivariate_feature_option): Add id by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#74](https://github.com/Flagsmith/flagsmith-engine/pull/74)
- Add django_id to feature state schema by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#78](https://github.com/Flagsmith/flagsmith-engine/pull/78)
- fix(mv_fs_value):uuid field by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#76](https://github.com/Flagsmith/flagsmith-engine/pull/76)
- Add engine tests by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#77](https://github.com/Flagsmith/flagsmith-engine/pull/77)
- fix(identity): dump identity features in a custom class by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#81](https://github.com/Flagsmith/flagsmith-engine/pull/81)
- Fix/mv schema/allow none for id field by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#80](https://github.com/Flagsmith/flagsmith-engine/pull/80)
- improve(fs/schema): Add validation for percentage allocation by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#82](https://github.com/Flagsmith/flagsmith-engine/pull/82)
- release 1.5.1 by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#75](https://github.com/Flagsmith/flagsmith-engine/pull/75)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.5.0...v1.5.1

[Changes][v1.5.1]

<a id="v1.5.0"></a>

## [Version 1.5.0 (v1.5.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.5.0) - 2021-12-15

## What's Changed

- feat(engine): move public environment function to engine (BREAKING CHANGE)
- feat(engine): Add support for hide_disabled_flags

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.4.3...v1.5.0

[Changes][v1.5.0]

<a id="v1.4.3"></a>

## [Version 1.4.3 (v1.4.3)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.4.3) - 2021-12-15

## What's Changed

- fix(identity/schema): use dump_default instead of default by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#65](https://github.com/Flagsmith/flagsmith-engine/pull/65)
- Allow custom identity schema by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#67](https://github.com/Flagsmith/flagsmith-engine/pull/67)
- feat(identity/model): Create custom class to hold identiy_features to basic checks by
  [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#69](https://github.com/Flagsmith/flagsmith-engine/pull/69)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.4.2...v1.4.3

[Changes][v1.4.3]

<a id="v1.4.2"></a>

## [Version 1.4.2 (v1.4.2)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.4.2) - 2021-12-07

## What's Changed

- Add integer IDs back to engine models by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#63](https://github.com/Flagsmith/flagsmith-engine/pull/63)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.4.1...v1.4.2

[Changes][v1.4.2]

<a id="v1.4.1"></a>

## [Version 1.4.1 (v1.4.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.4.1) - 2021-12-07

## What's Changed

- Upgrade marshmallow and pin in setup.py by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#60](https://github.com/Flagsmith/flagsmith-engine/pull/60)
- fix(ident/schema): allow none for django_id by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#59](https://github.com/Flagsmith/flagsmith-engine/pull/59)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.4.0...v1.4.1

[Changes][v1.4.1]

<a id="v1.4.0"></a>

## [Version 1.4.0 (v1.4.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.4.0) - 2021-12-06

## What's Changed

- Refactor django transformation logic to location outside of the core engine by
  [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#57](https://github.com/Flagsmith/flagsmith-engine/pull/57)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.3.4...v1.4.0

[Changes][v1.4.0]

<a id="v1.3.4"></a>

## [Version 1.3.4 (v1.3.4)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.3.4) - 2021-12-02

## What's Changed

- Fix json decimal encoder by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#54](https://github.com/Flagsmith/flagsmith-engine/pull/54)
- Fix feature states serialization for segments by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#51](https://github.com/Flagsmith/flagsmith-engine/pull/51)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.3.3...v1.3.4

[Changes][v1.3.4]

<a id="v1.3.3"></a>

## [Version 1.3.3 (v1.3.3)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.3.3) - 2021-11-30

## What's Changed

- feat(identity): Add uuid to identity model/schema by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#46](https://github.com/Flagsmith/flagsmith-engine/pull/46)
- Fix segment evaluation by casting condition value appropriately by [@matthewelwell](https://github.com/matthewelwell)
  in [Flagsmith/flagsmith-engine#48](https://github.com/Flagsmith/flagsmith-engine/pull/48)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.3.2...v1.3.3

[Changes][v1.3.3]

<a id="v1.3.2"></a>

## [Version 1.3.2 (v1.3.2)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.3.2) - 2021-11-30

## What's Changed

- Fix segment condition deserialization when property is None by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#44](https://github.com/Flagsmith/flagsmith-engine/pull/44)
- Add some end to end tests by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#40](https://github.com/Flagsmith/flagsmith-engine/pull/40)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.3.1...v1.3.2

[Changes][v1.3.2]

<a id="v1.3.1"></a>

## [Version 1.3.1 (v1.3.1)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.3.1) - 2021-11-29

## What's Changed

- Fix segment condition serialization when `property` is None by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#42](https://github.com/Flagsmith/flagsmith-engine/pull/42)
- Improve GitHub workflows by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#43](https://github.com/Flagsmith/flagsmith-engine/pull/43)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.3.0...v1.3.1

[Changes][v1.3.1]

<a id="v1.3.0"></a>

## [Version 1.3.0 (v1.3.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.3.0) - 2021-11-26

## What's Changed

- fix(ident/models): Allow trait value to support multiple type by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#39](https://github.com/Flagsmith/flagsmith-engine/pull/39)
- fix(schema/load_to_model): allow model_class to be none by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#38](https://github.com/Flagsmith/flagsmith-engine/pull/38)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.2.0...v1.3.0

[Changes][v1.3.0]

<a id="v1.2.0"></a>

## [Version 1.2.0 (v1.2.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.2.0) - 2021-11-25

## What's Changed

- Rename value -> feature_state_value for consistency by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#36](https://github.com/Flagsmith/flagsmith-engine/pull/36)
- feat(org/models): Add `get_unique_slug` used for tracking by [@gagantrivedi](https://github.com/gagantrivedi) in
  [Flagsmith/flagsmith-engine#29](https://github.com/Flagsmith/flagsmith-engine/pull/29)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.1.0...v1.2.0

[Changes][v1.2.0]

<a id="v1.1.0"></a>

## [Version 1.1.0 (v1.1.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.1.0) - 2021-11-25

## What's Changed

- Add update traits functionality by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#34](https://github.com/Flagsmith/flagsmith-engine/pull/34)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v1.0.0...v1.1.0

[Changes][v1.1.0]

<a id="v1.0.0"></a>

## [Version 1.0.0 (v1.0.0)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v1.0.0) - 2021-11-25

## What's Changed

- Add django_id attribute to identity document by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#27](https://github.com/Flagsmith/flagsmith-engine/pull/27)
- Remove dump from build model by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#31](https://github.com/Flagsmith/flagsmith-engine/pull/31)
- Move segment overrides to segment model by [@matthewelwell](https://github.com/matthewelwell) in
  [Flagsmith/flagsmith-engine#32](https://github.com/Flagsmith/flagsmith-engine/pull/32)

**Full Changelog**: https://github.com/Flagsmith/flagsmith-engine/compare/v0.1.2...v1.0.0

[Changes][v1.0.0]

<a id="v0.1.2"></a>

## [Version 0.1.2 (v0.1.2)](https://github.com/flagsmith/flagsmith-engine/releases/tag/v0.1.2) - 2021-11-24

## Release Notes

- Restrict dataclasses dependency to python<3.7

[Changes][v0.1.2]

[v5.3.0]: https://github.com/flagsmith/flagsmith-engine/compare/v5.2.0...v5.3.0
[v5.2.0]: https://github.com/flagsmith/flagsmith-engine/compare/v5.1.1...v5.2.0
[v5.1.1]: https://github.com/flagsmith/flagsmith-engine/compare/v5.1.0...v5.1.1
[v5.1.0]: https://github.com/flagsmith/flagsmith-engine/compare/v5.0.0...v5.1.0
[v5.0.0]: https://github.com/flagsmith/flagsmith-engine/compare/v4.1.0...v5.0.0
[v4.1.0]: https://github.com/flagsmith/flagsmith-engine/compare/v4.0.4...v4.1.0
[v4.0.4]: https://github.com/flagsmith/flagsmith-engine/compare/v4.0.3...v4.0.4
[v4.0.3]: https://github.com/flagsmith/flagsmith-engine/compare/v4.0.2...v4.0.3
[v4.0.2]: https://github.com/flagsmith/flagsmith-engine/compare/v4.0.1...v4.0.2
[v4.0.1]: https://github.com/flagsmith/flagsmith-engine/compare/v4.0.0...v4.0.1
[v4.0.0]: https://github.com/flagsmith/flagsmith-engine/compare/v3.6.0...v4.0.0
[v3.6.0]: https://github.com/flagsmith/flagsmith-engine/compare/v3.5.1...v3.6.0
[v3.5.1]: https://github.com/flagsmith/flagsmith-engine/compare/v3.5.0...v3.5.1
[v3.5.0]: https://github.com/flagsmith/flagsmith-engine/compare/v3.4.0...v3.5.0
[v3.4.0]: https://github.com/flagsmith/flagsmith-engine/compare/v3.3.2...v3.4.0
[v3.3.2]: https://github.com/flagsmith/flagsmith-engine/compare/v3.3.1...v3.3.2
[v3.3.1]: https://github.com/flagsmith/flagsmith-engine/compare/v3.3.0...v3.3.1
[v3.3.0]: https://github.com/flagsmith/flagsmith-engine/compare/3.2.0...v3.3.0
[3.2.0]: https://github.com/flagsmith/flagsmith-engine/compare/v3.1.0...3.2.0
[v3.1.0]: https://github.com/flagsmith/flagsmith-engine/compare/v3.0.0...v3.1.0
[v3.0.0]: https://github.com/flagsmith/flagsmith-engine/compare/v2.3.0...v3.0.0
[v2.3.0]: https://github.com/flagsmith/flagsmith-engine/compare/v2.2.0...v2.3.0
[v2.2.0]: https://github.com/flagsmith/flagsmith-engine/compare/v2.1.2...v2.2.0
[v2.1.2]: https://github.com/flagsmith/flagsmith-engine/compare/v2.1.1...v2.1.2
[v2.1.1]: https://github.com/flagsmith/flagsmith-engine/compare/v2.1.0...v2.1.1
[v2.1.0]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.7...v2.1.0
[v2.0.7]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.6...v2.0.7
[v2.0.6]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.5...v2.0.6
[v2.0.5]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.4...v2.0.5
[v2.0.4]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.3...v2.0.4
[v2.0.3]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.2...v2.0.3
[v2.0.2]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.1...v2.0.2
[v2.0.1]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.0-alpha.1...v2.0.1
[v2.0.0-alpha.1]: https://github.com/flagsmith/flagsmith-engine/compare/v2.0.0...v2.0.0-alpha.1
[v2.0.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.6...v2.0.0
[v1.6.6]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.5...v1.6.6
[v1.6.5]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.4...v1.6.5
[v1.6.4]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.3...v1.6.4
[v1.6.3]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.2...v1.6.3
[v1.6.2]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.1...v1.6.2
[v1.6.1]: https://github.com/flagsmith/flagsmith-engine/compare/v1.6.0...v1.6.1
[v1.6.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.5.1...v1.6.0
[v1.5.1]: https://github.com/flagsmith/flagsmith-engine/compare/v1.5.0...v1.5.1
[v1.5.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.4.3...v1.5.0
[v1.4.3]: https://github.com/flagsmith/flagsmith-engine/compare/v1.4.2...v1.4.3
[v1.4.2]: https://github.com/flagsmith/flagsmith-engine/compare/v1.4.1...v1.4.2
[v1.4.1]: https://github.com/flagsmith/flagsmith-engine/compare/v1.4.0...v1.4.1
[v1.4.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.3.4...v1.4.0
[v1.3.4]: https://github.com/flagsmith/flagsmith-engine/compare/v1.3.3...v1.3.4
[v1.3.3]: https://github.com/flagsmith/flagsmith-engine/compare/v1.3.2...v1.3.3
[v1.3.2]: https://github.com/flagsmith/flagsmith-engine/compare/v1.3.1...v1.3.2
[v1.3.1]: https://github.com/flagsmith/flagsmith-engine/compare/v1.3.0...v1.3.1
[v1.3.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.2.0...v1.3.0
[v1.2.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.1.0...v1.2.0
[v1.1.0]: https://github.com/flagsmith/flagsmith-engine/compare/v1.0.0...v1.1.0
[v1.0.0]: https://github.com/flagsmith/flagsmith-engine/compare/v0.1.2...v1.0.0
[v0.1.2]: https://github.com/flagsmith/flagsmith-engine/tree/v0.1.2

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.9.0 -->
