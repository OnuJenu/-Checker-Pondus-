Add support for uploading media files (voting_option) to the server while ensuring future extensibility for different storage providers.

Requirements:

File Uploads: In the first version, implement functionality to upload files directly to the server.
URL Handling: If the user provides a URL instead of a file, do not attempt to download the file. Use the URL as-is.
Extensibility for Storage Providers: Design the system to allow integration with various storage providers (e.g., Google Drive, Amazon S3) in the future, but do not implement these integrations at this stage.
Update Poll Route: Modify the route responsible for creating polls to support the updated file-upload logic.
Key Notes for Implementation:

Ensure a clean and modular design for future storage provider integrations.
Validate file uploads and URLs to maintain data integrity.
Optimize the API route to handle both file uploads and URLs seamlessly.
Let me know if you'd like further refinements or additional details.