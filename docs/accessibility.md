# Accessibility

## WCAG 2.2 AA Conformance

The publication-quality figures and interactive outputs produced by Skatteprogressivitet
target WCAG 2.2 Level AA conformance.

## Implemented Measures

| Criterion | Implementation |
|-----------|---------------|
| 1.1.1 Non-text content | ARIA `aria-label` on figure containers |
| 1.4.3 Contrast (minimum) | High-contrast sequential palette; min 4.5:1 ratio |
| 1.4.11 Non-text contrast | Chart borders and axes meet 3:1 ratio |
| 2.1.1 Keyboard | Keyboard navigation supported in interactive outputs |
| 2.4.6 Headings and labels | Descriptive axis labels and figure titles |
| 4.1.2 Name, Role, Value | `role="figure"` with `aria-label` on generated HTML figures |

## Colour Palette

Publication figures use a perceptually uniform sequential palette that avoids red-green
confusion and provides distinguishable steps in greyscale:

```
#003f5c -> #374c80 -> #7a5195 -> #bc5090 -> #ef5675 -> #ff764a -> #ffa600
```

## Known Limitations

- Full WCAG 2.2 AA conformance for complex Matplotlib/Plotly figures requires an
  axe-core audit. Automated audit is planned for integration in the CI pipeline.
- Static PNG fallbacks are provided for users who cannot access interactive outputs.

## Testing

Run the accessibility audit locally with:

```bash
npx axe docs/figures/ --wcag2aa
```
