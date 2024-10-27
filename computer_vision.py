import io  # Importing the io module for input/output operations (though not used here)
import contextlib
from dotenv import load_dotenv  # Importing load_dotenv to load environment variables from a .env file
from google.cloud import videointelligence  # Importing the Video Intelligence API client from Google Cloud

def main():
    # Create a Video Intelligence client
    video_client = videointelligence.VideoIntelligenceServiceClient()

    # Define features to be used for video annotation (label detection and object tracking)
    features = [
        videointelligence.Feature.LABEL_DETECTION,
        videointelligence.Feature.OBJECT_TRACKING
    ]
    
    # Specify the URI of the video file in Google Cloud Storage
    media_file = "gs://whack-mp4/mountain_biking1.mp4"

    # Start the video annotation operation
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": media_file}       
    )
    print('\nProcessing video for label and object tracking annotations:')

    # Wait for the operation to complete, with a timeout of 180 seconds
    result = operation.result(timeout=180)
    print('\nFinished processing.')

    # Extract the segment label annotations from the result
    segment_labels = result.annotation_results[0].segment_label_annotations

    # Process label detection results
    print("Label Detection Results:")
    for segment_label in segment_labels:
        # Print the description of the video label
        print('Video label description: {}'.format(segment_label.entity.description))

        # Loop through each category entity associated with the label
        for category_entity in segment_label.category_entities:
            print('\tLabel category: {}'.format(category_entity.description))

            # Loop through each segment within the label
            for i, segment in enumerate(segment_label.segments):
                # Calculate the start and end times of the segment in seconds
                start_time = (
                    segment.segment.start_time_offset.seconds
                    + segment.segment.start_time_offset.microseconds / 1e6
                )
                end_time = (
                    segment.segment.end_time_offset.seconds
                    + segment.segment.end_time_offset.microseconds / 1e6
                )

                # Format the time range for the segment
                positions = '{}s to {}s'.format(start_time, end_time)
                confidence = segment.confidence  # Get the confidence score for the segment

                # Print the segment details, including index, time range, and confidence
                print('\tSegment {}: {}'.format(i, positions))
                print('\tConfidence: {:.2f}'.format(confidence))
        print('\n')  # Print a newline for better readability between different labels

    # Process object tracking results
    print("Object Tracking Results:")
    object_annotations = result.annotation_results[0].object_annotations

    for object_annotation in object_annotations:
        # Print object description and confidence score
        print('Object description: {}'.format(object_annotation.entity.description))
        print('Confidence: {:.2f}'.format(object_annotation.confidence))

        # Loop through each frame where the object is detected
        for frame in object_annotation.frames:
            # Get the time offset of the frame in seconds
            time_offset = (
                frame.time_offset.seconds
                + frame.time_offset.microseconds / 1e6
            )
            # Get the normalized bounding box positions
            bounding_box = frame.normalized_bounding_box
            print('\tTime offset: {:.2f}s'.format(time_offset))
            print(
                '\tBounding box position - left: {:.2f}, top: {:.2f}, right: {:.2f}, bottom: {:.2f}'.format(
                    bounding_box.left,
                    bounding_box.top,
                    bounding_box.right,
                    bounding_box.bottom
                )
            )
        print('\n')  # Print a newline for better readability between different objects

if __name__ == '__main__':
    load_dotenv('credentials.env')  # Load the environment variables from the specified .env file
    main()  # Call the main function to execute the video annotation process
    # Redirect all prints to agent_message.txt
    with open("agent_message.txt", "w") as f:
        with contextlib.redirect_stdout(f):
            main()
