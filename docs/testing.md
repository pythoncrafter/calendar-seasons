# Testing and release matrix

Automated scripts: `npm test` validates theme/date logic, malformed settings, custom palettes, resource parity, JavaScript syntax, JSON, XML/SVG, plists/privacy manifests, manifest resource paths, and Xcode object references. These are not an Xcode compilation. `npm run test:browser` loads the actual unpacked extension in Chromium and uses an intercepted synthetic Calendar page; it tests preferences, theme application, preserved event color, editable dialog, navigation replacement, reset, reload, dark/reduced-motion media, and narrow/landscape viewport layout. It does not access an authenticated Google account. When unpacked extensions are administratively blocked, `npm run test:fixture` exercises the same shared scripts and UI using simulated storage/runtime APIs. That fallback does not test browser extension activation.

Run the following manually in current desktop Chrome and physical iPhone Safari. **All live Google and Safari rows are pending** until a tester records results.

| Check | Procedure | Expected |
|---|---|---|
| Activation | Enable extension and allow Calendar website | Settings popup opens; calendar gets theme |
| Mobile DOM | Open signed-in site in portrait/landscape, record structural hooks and route | Unsupported layouts stay usable; styling limits recorded |
| Four themes | Choose each card | Distinct illustrations and palette; selection state correct |
| Persistence | Change color/intensity; close browser and reopen | Same saved preferences |
| Automatic | Enable schedule, test month boundaries and local time zone via engine or test device | Winter Dec–Feb, Spring Mar–May, Summer Jun–Aug, Fall Sep–Nov |
| Custom mapping | Change month to another season | Resolves correctly; selecting theme turns automatic off |
| Motion | Minimal/Cozy/Magical; toggle animation and reduced motion | Only Magical animates; either reduced-motion setting stops effects |
| Background tab | Switch tabs while Magical enabled | Effects pause; resume when visible |
| Reset | Choose Default Google appearance | No overlay or scoped surface attributes; original appearance restored |
| Re-enable | Bring back seasons; disable/enable browser extension; reload | Restores saved preferences; browser disable may require reload |
| Views | Navigate day/week/month, agenda if available, today, previous/next | No broken navigation or scroll |
| Event workflow | Create, edit, delete a disposable test event | Native functionality and event colors preserved |
| Search/dialogs | Search, open settings, popup details, edit dialog | Controls, keyboard focus and touch unaffected |
| Appearances | Test OS light/dark against Google's light/dark setting | Text remains readable; record native theme mismatch |
| Custom colors | Very light/dark background, accent and surface | Inspect native labels; restore palette if contrast decreases |
| Dynamic DOM | Change view repeatedly and reload | New semantic surfaces get styled; no duplicated overlay |
| Touch/keyboard | Tap event near decor, drag/scroll, tab through desktop controls | Decor never intercepts input |
| Accessibility | VoiceOver settings labels, large text, system reduce motion, forced colors | Usable settings; effects hidden/reduced |
| Permissions | Deny and later allow website access | Calendar still works; extension starts only after access |
| Xcode release | Build, archive, inspect embedded resources, install signed build | Successful Apple build and real device activation |

Record test date, browser/OS versions, outcome and limitations in `docs/validation-results.md`. Do not paste real calendar content into logs.
