import os
import subprocess

# def generate_ffmpeg_input_file(media_sets, input_file):
#     """
#     Generate an FFmpeg input file for concatenating image and audio pairs.
#     """
#     with open(input_file, 'w') as f:
#         for index, media in enumerate(media_sets):
#             f.write(f"file '{media['image']}'\n")
#             f.write(f"duration {media['duration']}\n")
#             if index == len(media_sets) - 1:  # Last image
#                 f.write(f"file '{media['image']}'\n")  # Hold the last frame

def create_video_with_audio(media_sets, output_file):
    """
    Create a video from a series of images and corresponding audio files using FFmpeg.
    """
    for index, media in enumerate(media_sets):
        image = media['image']
        audio = media['audio']
        output = f"temp_{index}.mp4"
        
        # Generate video clip for each image and audio pair
        # cmd = [
        #     "ffmpeg",
        #     "-y",
        #     "-loop", "1",  # Loop the image
        #     "-i", image,  # Input image
        #     "-i", audio,  # Input audio
        #     "-c:v", "libx264",
        #     "-c:a", "aac",
        #     "-b:a", "192k",
        #     "-shortest",  # End the video when the audio ends
        #     output
        # ]
        # subprocess.run(cmd, check=True)
        command_str = 'sudo ffmpeg -y -loop "1" -i "' + str(image) + '" -i "'+ str(audio) + '" -c:v "libx264" -c:a "aac" -b:a "192k" -shortest "' + str(output) + '"'
        # ffmpeg -y -loop "1" -i "res/0_vid/images/0.jpg" -i "res/0_vid/speech/0.mp3" -c:v "libx264" -c:a "aac" -b:a "192k" -shortest "final_video.mp4" 2> ffmpeg_log.log
        subprocess.run(command_str, shell=True)
        print('---- INTERMEDIATE FILE SIZES ---')
        print(output + ': ' + str(os.path.getsize(str(output))))
    # Create a list file for concatenation
    list_file = "concat_list.txt"
    with open(list_file, 'w') as f:
        for index in range(len(media_sets)):
            f.write(f"file 'temp_{index}.mp4'\n")

    # Concatenate all video segments
    print('------concat list ------')
    with open('concat_list.txt', 'r') as file:
        print(file.read())
    # concat_cmd = [
    #     "ffmpeg",
    #     "-y",
    #     "-f", "concat",
    #     "-safe", "0",
    #     "-i", list_file,
    #     "-filter_complex", "[0:v]fade=t=in:st=0:d=1[v0];[0:v]fade=t=out:st=4:d=1[v1]",
    #     "-vf", "scale=1080:1920",  # Set the output resolution
    #     "-c:v", "libx264",
    #     "-c:a", "aac",
    #     output_file
    # ]

    # concat_cmd = [
    # "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "concat_list.txt",
    # "-filter_complex", """
    #     [0:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v0];
    #     [v0]format=yuv420p[v];
    #     [0:a]afade=t=in:st=0:d=1,afade=t=out:st=4:d=1[a]
    # """,
    # "-map", "[v]", "-map", "[a]", "-vf", "scale=1080:1920", "-c:v", "libx264",
    # "-c:a", "aac", "final_video.mp4", "-loglevel", "debug"
    # ]
    
    # subprocess.run(concat_cmd, check=True)
    # subprocess.run('sudo ffmpeg -y -f "concat" -safe "0" -i "concat_list.txt" -filter_complex "[0:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v0];[v0]format=yuv420p[v];[0:a]afade=t=in:st=0:d=1,afade=t=out:st=4:d=1[a]" -map "[v]" -map "[a]" -vf "scale=1080:1920" -c:v "libx264" -c:a "aac" "final_video.mp4" -loglevel "debug"', shell=True)
    # subprocess.run('sudo ffmpeg -y -f "concat" -safe "0" -i "concat_list.txt" -filter_complex "[0:v]fade=t=in:st=0:d=1[v0];[0:v]fade=t=out:st=4:d=1[v1]" -vf "scale=1080:1920" -c:v "libx264" -c:a "aac" "final_video.mp4"', shell=True)
    subprocess.run('sudo ffmpeg -y -f "concat" -safe "0" -i "concat_list.txt" -vf "scale=1080:1920" -c:v "libx264" -c:a "aac" "'+output_file+'"', shell=True)
    # subprocess.run(concat_cmd, check=True)

    # subprocess.run('sudo ffmpeg -y -f "concat" -safe "0" -i "concat_list.txt" -filter_complex "[0:v]fade=t=in:st=0:d=1[v0];[0:v]fade=t=out:st=4:d=1[v1]" -vf "scale=1080:1920" -c:v "libx264" -c:a "aac" "final_video.mp4"', shell=True)

    # Clean up temporary files
    for index in range(len(media_sets)):
        os.remove(f"temp_{index}.mp4")
    os.remove(list_file)


def run_editor(media_sets, output_file):
    # media_sets = [
    #     {"image": "image1.jpg", "audio": "audio1.mp3"},
    #     {"image": "image2.jpg", "audio": "audio2.mp3"},
    #     {"image": "image3.jpg", "audio": "audio3.mp3"},
    # ]
    # output_file = "final_video.mp4"
    create_video_with_audio(media_sets, output_file)
