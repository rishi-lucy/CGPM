# Task: Add pic and video upload by admin and view by citizen

## Implementation Steps

### Step 1: Update Database Model (app.py)
- [x] Add `admin_image_path` column to Complaint model

### Step 2: Update Assign Route (app.py)
- [x] Modify `/admin/assign/<complaint_id>` route to handle file upload
- [x] Add file upload logic for admin evidence

### Step 3: Update Admin Assign Template (templates/assign_complaint.html)
- [x] Add file upload section for admin to upload pic/video
- [x] Include file preview functionality

### Step 4: Update Citizen Track Template (templates/track_complaint.html)
- [x] Display citizen uploaded evidence (existing)
- [x] Display admin uploaded evidence (new)

## Status: Completed ✅

