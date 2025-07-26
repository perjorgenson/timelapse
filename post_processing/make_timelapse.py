import cv2
from pathlib import Path
from datetime import datetime

def create_timelapse(input_dir, output_video_path="timelapse.mp4", fps=30, frame_size=None):
    input_dir = Path(input_dir)
    image_files = sorted(
        [f for f in input_dir.glob("photo_*.jpg")],
        key=lambda f: datetime.strptime(f.name, "photo_%Y-%m-%d_%H-%M-%S.jpg")
    )

    if not image_files:
        raise ValueError("No images found in the specified directory with the expected filename format.")

    # Read the first image to get the size
    first_frame = cv2.imread(str(image_files[0]))
    if first_frame is None:
        raise ValueError(f"Could not read image: {image_files[0]}")

    height, width = first_frame.shape[:2]
    if frame_size is None:
        frame_size = (width, height)

    # Define the codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    for img_path in image_files:
        frame = cv2.imread(str(img_path))
        if frame is None:
            print(f"Warning: Could not read image {img_path}, skipping.")
            continue
        resized_frame = cv2.resize(frame, frame_size)
        out.write(resized_frame)

    out.release()
    print(f"Timelapse video saved to {output_video_path}")
create_timelapse("/path/to/images", "my_timelapse.mp4", fps=10)
# Example usage
# create_timelapse("/path/to/images", "my_timelapse.mp4", fps=30)
