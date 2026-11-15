# 07 — ProcessScope dashboard refinement

The application is now called ProcessScope. Its compact header replaces the large banner; the navigation tabs have more room and the interface uses a distinctive local serif heading and monospaced metrics alongside a readable system UI font. No font downloads are required.

The sidebar offers a light/dark switch, and its built-in arrow collapses or reopens the sidebar. Charts use colors appropriate to the selected appearance. This preference lasts for the current browser session.

The refresh interval now defaults to 2 seconds, with 1 second as the fastest option. Static branding and the header sit outside the periodically updated area, and the metric cards no longer replay an entrance animation with each update. Changing sidebar controls reuses the most recent snapshot until the interval expires, rather than collecting and storing additional samples on each interaction.
