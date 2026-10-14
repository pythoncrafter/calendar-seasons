# Compatibility and troubleshooting

## Conservative styling

The content script runs only on `https://calendar.google.com/*`, in the top frame. It reads semantic element structure, never calendar text or private event attributes. It adds a scoped attribute to `main`, `[role=main]`, and grids that contain grid cells or column headers. It leaves dialog contents, individual event backgrounds, event handlers, navigation, scrolling, and keyboard input untouched. SVG decor lives in a closed shadow root with pointer events disabled. Unknown mobile layouts get background/decor only; they are not rewritten to mimic desktop Calendar.

Google may paint opaque child surfaces over themed containers. This is an intentional conservative limitation: decorations and coordinated outer surfaces remain, but some calendar cells, navigation controls, or event chips stay native. Google changing its DOM can reduce styling. Do not add obfuscated class-name selectors as a quick fix; inspect new semantic hooks and rerun the interaction matrix first.

The OS light/dark preference selects default palettes. Native Google appearance can differ from the OS setting; verify readability in both combinations before release. A contrast guard skips background/surface styling when the container’s native text has less than 4.5:1 contrast against the selected color. Google’s explicitly colored descendant labels still require manual readability checks. Restore seasonal colors if labels become hard to read. Event chip colors are not changed by the extension.

## Mobile verification status

An iPhone Safari user-agent request to Google Calendar was attempted in this environment. The initial attempt failed at the configured network proxy. A follow-up request succeeded and redirected to Google Calendar sign-in (HTTP 200 after three redirects), with no calendar grids in the returned markup. No authenticated iPhone DOM, Safari rendering, or mobile event workflow was observed. Chromium viewport tests against synthetic semantic/legacy fixtures are not Safari verification. A physical iPhone with an authenticated Google account is required to establish which current mobile routes expose supported hooks. Record the URL, iOS version, chosen view, and hook availability without recording event data. If the mobile site redirects to another hostname, the extension does not run there: host permissions intentionally remain limited to calendar.google.com. Request Desktop Website can be tried manually, but is not guaranteed or automatically forced.

## Common issues

- No theme: enable the extension, allow this website, confirm the hostname, and reload. Check that **Default Google appearance** is not selected.
- Colors change unexpectedly: **Follow the seasons** is enabled. Selecting a theme creates a manual override.
- No floating effect: select **Magical**, enable animations, disable extra gentle motion, and check device reduced-motion preferences. Effects pause while the tab is hidden.
- Sparse mobile styling: unsupported elements remain native; decorations still avoid blocking interaction.
- Save failed: reopen the popup; browser storage may be unavailable or the extension may have been disabled.
- Development edits not visible: run `npm run build`, reload the extension, then reload Calendar. Updating Safari resources requires rebuilding the app in Xcode.

There is no content collection or debug export. To troubleshoot private calendars, use an empty test calendar and structural observations rather than screenshots with personal events.
