from tkinter import Image
from app.utils.validation import check_file_extension
from werkzeug.utils import secure_filename

class MediaProcessor:
    def __init__(self, upload_folder):
        self.media_service = MediaService(upload_folder)
    
    def process_media_file(self, file, poll_id):
        """
        Processes the uploaded media file based on its type.
        :param file: The uploaded file object
        :param poll_id: The ID of the poll associated with this media
        :return: The path to the processed media file or None if processing fails
        """
        return self.media_service.process_media_file(file, poll_id)
    
    def optimize_image(self, image_path):
        """
        Optimizes an image by resizing it to a standard format.
        :param image_path: The path to the image file
        :return: The path to the optimized image file
        """
        return self.media_service.optimize_image(image_path)
    
    def optimize_video(self, video_path):
        """
        Optimizes a video by compressing it.
        :param video_path: The path to the video file
        :return: The path to the optimized video file
        """
        return self.media_service.optimize_video(video_path)
    
    def delete_media_file(self, file_path):
        """
        Deletes a media file.
        :param file_path: The path to the file
        """
        self.media_service.delete_media_file(file_path)

def process_media_file(file, poll_id=None):
    # Logic to process media file
    processor = MediaProcessor(upload_folder='/path/to/upload/folder')
    return processor.process_media_file(file, poll_id)

def optimize_media(file_path):
    # Logic to optimize media
    processor = MediaProcessor(upload_folder='/path/to/upload/folder')
    if os.path.splitext(file_path)[1] in ['.png', '.jpg', '.jpeg', '.gif']:
        return processor.optimize_image(file_path)
    elif os.path.splitext(file_path)[1] == '.mp4':
        return processor.optimize_video(file_path)

class MediaService:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav'}

    def process_media_file(self, file, poll_id):
        filename = secure_filename(file.filename)
        file_path = os.path.join(self.upload_folder, filename)

        # Validate file extension and size
        if not check_file_extension(filename, self.allowed_extensions):
            raise ValueError("Unsupported file format")
        
        file.save(file_path)

        # Optimize the media based on its type
        if file.content_type.startswith('image'):
            optimized_path = self.optimize_image(file_path)
        elif file.content_type.startswith('video'):
            optimized_path = self.optimize_video(file_path)
        else:
            return file_path

        return optimized_path

    def optimize_image(self, image_path):
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.thumbnail((1024, 1024), Image.ANTIALIAS)
            base_filename, ext = os.path.splitext(os.path.basename(image_path))
            new_image_path = os.path.join(self.upload_folder, f"{base_filename}_optimized{ext}")
            img.save(new_image_path)

        return new_image_path

    def optimize_video(self, video_path):
        clip = mp.VideoFileClip(video_path)
        optimized_clip = clip.resize(height=480)  # Resize to a standard height
        base_filename, ext = os.path.splitext(os.path.basename(video_path))
        new_video_path = os.path.join(self.upload_folder, f"{base_filename}_optimized{ext}")
        optimized_clip.write_videofile(new_video_path, codec='libx264')

        return new_video_path

    def delete_media_file(self, file_path):
        os.remove(file_path)