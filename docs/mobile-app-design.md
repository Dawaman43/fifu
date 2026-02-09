# Fifu Mobile App Design (Draft)

## Product Goal
A fast, clear controller for channel and playlist downloads, with real-time progress and a simple library of recent and favorite channels.

## Information Architecture
1. Home (Search)
2. Results (Channel list)
3. Options (Quality, count, playlist, subtitles)
4. Downloads (Queue, per-item progress, log)
5. Library (History, Favorites)
6. Settings (Defaults, storage, concurrency)

## Visual System
- Style: bold minimal utility
- Fonts: Space Grotesk for headings, Inter for body
- Icon set: Lucide (consistent stroke)
- Background: #FDF2F3
- Surface: #FFF9FA
- Text: #3A0B14
- Muted text: #7A3A46
- Primary: #E11D48
- Secondary: #FB7185
- CTA: #2563EB
- Borders: 1px, low contrast, no pure black or white
- Spacing: 4px scale only

## Navigation
- Bottom tabs: Home, Downloads, Library, Settings
- Results and Options are pushed screens from Home

## Core Screens

Home (Search)
- Search input with scan-friendly placeholder
- Recent list, then Favorites list
- Each row shows name and sub count
- Primary action: Search button

Results
- Card list with channel name, subs, short description
- Favorite toggle on each item
- Tap to open Options

Options
- Video count input with quick chips: 5, 10, 25, All
- Quality picker (radio list)
- Subtitles toggle
- Playlist picker when available
- Primary CTA: Start Download

Downloads
- Overall progress bar with counts
- Active downloads list with per-item progress, speed, ETA
- Expandable log panel
- Stop queue button

Library
- Segmented control: History, Favorites
- Each row has quick actions: Open Options, Remove

Settings
- Default quality
- Subtitle default
- Max concurrency
- Download path
- Clear logs and history

## Component Notes
- Buttons use high-contrast CTA color and 44px minimum touch targets
- Inputs show clear focus and validation state
- Cards use subtle borders and slight elevation only in light mode
- Use skeleton loaders for search results and downloads list

## Motion
- 200ms ease-in-out for transitions
- Use opacity and translate only
- Respect reduced motion

## Accessibility
- Minimum 4.5:1 contrast
- All controls 44x44 minimum
- Clear focus rings for keyboard and accessibility tooling
