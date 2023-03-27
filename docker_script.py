from behave.parser import parse_file
from environment import Configuration as cfg
import os
import itertools
import multiprocessing
import subprocess
import time
import click


@click.command()
@click.option('--docker_parallel_video', default=False, help='Whether to run tests in a Docker container or not')
@click.option('--docker_compose', default=False, help='Whether to run tests in a Docker container or not')
def run(docker_parallel_video='', docker_compose=''):

    if docker_parallel_video:
        # set the variable so that the framework will know to use remote webdriver
        os.environ["docker_parallel_video"] = "True"

        # run the tests
        feature_files = get_feature_files()
        tags = get_parallel_tags(feature_files)
        run_parallel_tags(tags)
    elif docker_compose:
        os.environ["docker_compose"] = "True"
        subprocess.run(["docker", "compose", "-f", "docker-compose-v3.yml", "up", "-d"])
        time.sleep(5)
        subprocess.run(["behave", "--tags", "~all"])
        subprocess.run(["docker", "compose", "-f", "docker-compose-v3.yml", "down"])
    else:
        subprocess.run(["behave", "--tags", "~all"])


def get_feature_files():
    test_dir = os.path.join(os.getcwd(), "tests")
    feature_files = [
        os.path.join(test_dir, f)
        for f in os.listdir(test_dir)
        if f.endswith(".feature")
    ]
    return feature_files


def get_parallel_tags(feature_files):
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
    tags = [f"{tag}" for tag in tags_list if tag.startswith("parallel_")]
    return tags


def run_parallel_tags(tags):

    container_ports = itertools.cycle([4440, 4441, 4442, 4443, 4444])
    video_ports = itertools.cycle([5900, 5901, 5902, 5903, 5904])

    pool = multiprocessing.Pool(cfg.MAX_PARALLEL_SCENARIOS)
    for tag in tags:
        container_port = next(container_ports)
        video_port = next(video_ports)
        pool.apply_async(run_feature, args=(tag, container_port, video_port))
    pool.close()
    pool.join()


def run_feature(tag, container_port, video_port):

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
            "./Scenario_videos:/videos",
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
    run()
