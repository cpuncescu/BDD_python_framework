from behave.parser import parse_file
import os
import multiprocessing
import subprocess
import time


def run_feature(tag, container_port, video_port):
    #get the path one level above the current path so that we can store the videos there
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    container_name = f"selenium_{tag}"

    os.environ["ports"] = str(container_port)

    subprocess.run(["docker", "network", "create", f"selenium_grid_{tag}"])

    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-p",
            f"{container_port}:4444",
            "-p",
            f"{video_port}:5900",
            "--net",
            f"selenium_grid_{tag}",
            "--name",
            container_name,
            "--shm-size=2g",
            "selenium/standalone-chrome:latest",
        ]
    )
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--net",
            f"selenium_grid_{tag}",
            "--name",
            f"video_{tag}",
            "-v",
            f"{parent_dir}/Scenario_videos:/videos",
            "-e",
            f"DISPLAY_CONTAINER_NAME={container_name}",
            "-e",
            f"FILE_NAME=video_{tag}.mp4",
            "selenium/video:ffmpeg-4.3.1-20230306",
        ]
    )
    time.sleep(5)
    subprocess.run(["behave", "--tags", tag])
    # stop and remove video container
    subprocess.run(["docker", "stop", f"video_{tag}"])
    subprocess.run(["docker", "rm", f"video_{tag}"])

    # stop and remove selenium container
    subprocess.run(["docker", "stop", container_name])
    subprocess.run(["docker", "rm", container_name])

    # stop and remove the grid
    subprocess.run(["docker", "network", "rm", f"selenium_grid_{tag}"])


if __name__ == "__main__":
    feature_files = [
        os.path.join(os.getcwd(), f)
        for f in os.listdir(os.getcwd())
        if f.endswith(".feature")
    ]
    # Set to store all tags
    tags_list = set()

    # Loop through each feature file
    for feature_file in feature_files:
        # Parse the feature file
        feature = parse_file(feature_file)

        # Loop through each scenario in the feature file
        for scenario in feature.walk_scenarios():
            # Add all the tags from the scenario to the set
            tags_list.update(scenario.tags)
    # Convert the set to a list
    tags = [f"{tag}" for tag in tags_list if tag.startswith("parallel")]
    container_ports = [4440, 4441, 4442, 4443, 4444]
    video_ports = [5900, 5901, 5902, 5903, 5904]

    pool = multiprocessing.Pool(3)
    for tag, container_port, video_port in zip(tags, container_ports, video_ports):
        pool.apply_async(run_feature, args=(tag, container_port, video_port))
    pool.close()
    pool.join()
