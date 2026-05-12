---
name: Legislative-parameter update
about: Propose a new or revised legislation YAML file
labels: legislation
---

**Year**
<!-- Which reform year does this update cover? -->

**SFS reference**
<!-- e.g. SFS 2024:875 -->

**Prop. reference**
<!-- e.g. Prop. 2024/25:1 -->

**Effective date**
<!-- e.g. 2025-01-01 -->

**Summary of changes**
<!-- Which parameters changed from the previous year? -->

**Source documentation**
<!-- Link to the official SFS text or Regeringskansliet proposition. -->

**Checklist**
- [ ] YAML file follows the ledger schema (`data/legislation/schema.json`)
- [ ] SFS and Prop. references included in YAML header comments
- [ ] `skatteprogressivitet validate-legislation --year <year>` passes
- [ ] Tests updated if new parameter fields added
