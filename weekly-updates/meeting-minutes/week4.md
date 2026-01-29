# Meeting Notes- Jan 27th 2026

### General app discussion

- Started off by finalizing memory map idea
- Original app idea is that the app is a mobile-first memory mapping application that allows users to capture and revisit memories (photos, captions, and voice memos) tied to physical locations over time, through a visual map experience
- Considered backend/frontend components and integration
- Discussed to keep the backend lightweight by having the media memories linked to the phone’s local storage and so when the app is reopened, memories are reloaded from the device rather than a heavy centralized backend
  - That way Cloud services are optional and primarily used for sharing and syncing shared maps
  - This was scrapped with the idea of having collaborative maps, explore page, etc we'd need a backend to store it

### Discussion of Core Features (Initial + Planned)

- Memory Capture
- Capture photos directly from the app
- Attach captions or longer text notes
- Record voice memos associated with a memory
- Automatically tag memories with location (GPS) and time
- Memory Visualization
- Map View
- Displays memories as pins on a map
- Optional lines showing movement over time (travel paths/timelines)
- List / Timeline View
- Chronological list of memories
- Nested lists for shared maps
- Explore / Photo Feed View
- Scrollable feed of photos within a specific map
- Click into individual photos to view details (caption, audio, author, timestamp)
- Organization & Filtering
- Filter memories by: Time range, Location, Associated friend or shared map
- Support both: Personal maps (private memory collections), Shared maps (group travel or collaborative albums)
  ###Notifications & Mobile-Specific Features
- The app leverages mobile capabilities to enhance the experience:
- Location-based notifications
- Prompt users to capture memories when entering a new place
- “Remember this place” prompts when visiting frequently visited locations
- Time-based notifications
- Daily or weekly recap notifications once the user returns home
- These features reinforce why the app makes sense as a native mobile app

### Permissions & Privacy Considerations

- Key permissions and considerations:
- Location (GPS) — required for mapping and geofence-based prompts
- Camera — required for photo capture
- Microphone — required for voice memos
- Contacts — optional, used to discover friends already using the app
- Clear user consent and transparency around permission usage
  ###External Services & APIs
- For the actual UI we'd need Google Maps API (or equivalent) for:
- Map rendering
- Location identification (for notifications for new places)
- Optional cloud storage for:
- Media uploads
- Shared map synchronization

### User Experience & Visual Design

- Main screen with map view
- Toggleable list/timeline view
- Shared maps overview
- Photo feed (Instagram-style scroll) within a map
- Detailed memory view (photo, caption, voice memo, metadata)

### Team Responsibilities

Design & UX: Alex, Amirdha

Use Case Diagrams & UML: Chiara, Helena

Requirements & Timeline Planning: Aaryan, Priyanshu
