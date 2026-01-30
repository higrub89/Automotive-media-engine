# Frontend Development Plan: AutoMedia UI

## Context
We are building a **React/Next.js** web interface for the `automotive-media-engine`. The backend is a standard FastAPI service with Swagger documentation available at `/docs`.

**Goal:** Create a simple, robust dashboard where users can generate videos, monitor progress in real-time, and download the results without touching the command line.

**Constraint:** The backend is running on a low-cost VPS. The frontend should be lightweight and efficiently poll for status updates.

---

## 📅 Handoff Checklist for Alex

### 1. API Integration Points
The backend exposes the following endpoints (defined in `api/router.py`):

*   `POST /generate`: Triggers a new video job.
    *   **Payload:**
        ```json
        {
          "topic": "The Future of Solid State Batteries",
          "style_archetype": "technical", // technical | storytelling | documentary | minimalist
          "duration": 60,
          "platform": "linkedin"
        }
        ```
    *   **Returns:** `{"job_id": "uuid-string", "status": "processing"}`

*   `GET /status/{job_id}`: Poll this endpoint every 2-3 seconds for updates.
    *   **Returns:**
        ```json
        {
          "job_id": "uuid...",
          "status": "processing", // queued | processing | completed | failed
          "progress": 45,         // Integer 0-100
          "status_message": "Visualizing scene 2/5...", // Granular update string
          "output_url": "https://...", // Present only when status=completed
          "error": null
        }
        ```

### 2. UI/UX Requirements

#### A. "New Video" Dashboard (Home)
*   **Simple Form:**
    *   **Topic Input:** Text field (e.g., "Quantum Computing in EV Motors").
    *   **Style Selector:** Dropdown/Cards for the 4 archetypes (Technical, Storytelling, etc.).
    *   **Duration Slider:** 15s to 180s (Default: 60s).
    *   **Generate Button:** Big, prominent call-to-action.

#### B. "Live Progress" Modal/Card
*   **Real-time Feedback:** When "Generate" is clicked, show a progress bar.
    *   Bind the `progress` (0-100%) to the bar width.
    *   Display `status_message` just below (e.g., "Generating script...").
    *   **Do NOT** block the UI. Allow the user to start another video while one is processing.

#### C. "Video Library" (History)
*   **List View:** Show recent jobs.
*   **Status Indicators:**
    *   🟢 Completed
    *   🟡 Processing (with %)
    *   🔴 Failed (hover for error message)
*   **Actions:**
    *   **Download:** Direct link to `output_url` (R2/S3 link).
    *   **Play:** Embedded HTML5 video player for quick preview.

### 3. Technical Implementation Steps

1.  **Framework:** Initialize a Next.js 14 project (App Router) with Tailwind CSS.
    *   `npx create-next-app@latest auto-media-ui --typescript --tailwind --eslint`

2.  **API Client:** Create a typed API client (using Axios or Fetch).
    *   Define the `VideoStatus` interface matching the backend Pydantic model.

3.  **State Management:**
    *   Use React Query (TanStack Query) for polling `GET /status/{job_id}`.
    *   Configure refetch interval to 2000ms.

4.  **Deployment:**
    *   Deploy as a static export or simple Node app to Vercel (easiest) or the same Hetzner VPS (cheapest).

### 4. Mock Data for Development
Since the backend might not be online 24/7 during dev, use this mock response for `GET /status/mock-id`:

```json
{
  "job_id": "mock-id",
  "status": "processing",
  "progress": 65,
  "status_message": "Rendering 3D animations...",
  "output_url": null
}
```

---

**Note to Alex:** Focus on *feedback*. The backend can take 1-2 minutes to generate a video. The user needs to know the system hasn't crashed. The `status_message` field is your best friend here.
