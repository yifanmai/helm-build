# Uses the marin-cluster-template.yaml file to create the three cluster configuration files.
import os

import jinja2
import yaml

this_path = os.path.dirname(os.path.abspath(__file__))

cluster_template_path = os.path.join(this_path, "marin-cluster-template.yaml")
vllm_template_path = os.path.join(this_path, "marin-vllm-template.yaml")

LATEST = "20250721"  # The latest docker tag used for the clusters, update this when you update the docker image.

configs = {
    "marin-us-central2": {
        "NAME": "marin-us-central2",
        "REGION": "us-central2",
        "ZONE": "us-central2-b",
        "BUCKET": "marin-us-central2",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v4",
        "min_workers": 4,
    },
    "marin-us-central2-compress": {
        "NAME": "marin-us-central2-compress",
        "REGION": "us-central2",
        "ZONE": "us-central2-b",
        "BUCKET": "marin-us-central2",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v4",
        "min_workers": 4,
    },
    "marin-us-central1": {
        "NAME": "marin-us-central1",
        "REGION": "us-central1",
        "ZONE": "us-central1-a",
        "BUCKET": "marin-us-central1",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v5p",
        "min_workers": 1,
        "worker_targets": {
            "v5p-8": 12,
            "v5p-16": 1,
            "v5p-32": 1,
            "v5p-64": 1,
            "v5p-128": 0,
            "v5p-256": 0,
            "v5p-512": 0,
        },
    },
    "marin-big-run": {
        "NAME": "marin-big-run",
        "REGION": "us-central2",
        "ZONE": "us-central2-b",
        "BUCKET": "marin-us-central2",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v4",
        "min_workers": 0,
    },
    "marin-eu-west4": {
        "NAME": "marin-eu-west4",
        "REGION": "europe-west4",
        "ZONE": "europe-west4-b",
        "BUCKET": "marin-eu-west4",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v5e",
        "min_workers": 0,
        "worker_targets": {
            "v5e-128": 1,
        },
    },
    "marin-us-west4": {
        "NAME": "marin-us-west4",
        "REGION": "us-west4",
        "ZONE": "us-west4-a",
        "BUCKET": "marin-us-west4",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v5e",
        "min_workers": 0,
    },
    "marin-us-east1": {
        "NAME": "marin-us-east1-d",
        "REGION": "us-east1",
        "ZONE": "us-east1-d",
        "BUCKET": "marin-us-east1",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v6e",
        "min_workers": 0,
        "worker_targets": {
            "v6e-128": 8,
        },
    },
    "marin-us-east5": {
        "NAME": "marin-us-east5",
        "REGION": "us-east5",
        "ZONE": "us-east5-b",
        "BUCKET": "marin-us-east5",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v6e",
        "min_workers": 0,
        "worker_targets": {
            "v6e-128": 8,
        },
    },
    "marin-us-east5-a": {
        "NAME": "marin-us-east5-a",
        "REGION": "us-east5",
        "ZONE": "us-east5-a",
        "BUCKET": "marin-us-east5",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v5p",
        "min_workers": 4,
        "worker_targets": {
            "v5p-2048": 2,
        },
    },
    "marin-eu-west4-a": {
        "NAME": "marin-eu-west4-a",
        "REGION": "europe-west4",
        "ZONE": "europe-west4-a",
        "BUCKET": "marin-eu-west4",
        "DOCKER_TAG": LATEST,
        "tpu_generation": "v6e",
        "min_workers": 0,
        "worker_targets": {
            "v6e-128": 2,
        },
    },
    "marin-us-east5-b-vllm": {
        "NAME": "marin-us-east5-b-vllm",
        "REGION": "us-east5",
        "ZONE": "us-east5-b",
        "BUCKET": "marin-us-east5",
        "DOCKER_TAG": "6e804a10",
        "tpu_generation": "v6e-serve",
        "min_workers": 2,
        "VLLM": True,
    },
    "marin-eu-west4-vllm": {
        "NAME": "marin-eu-west4-vllm",
        "REGION": "europe-west4",
        "ZONE": "europe-west4-b",
        "BUCKET": "marin-eu-west4",
        "DOCKER_TAG": "7fab502e",
        "tpu_generation": "v5e",
        "min_workers": 2,
        "VLLM": True,
    },
    "marin-us-central2-vllm": {
        "NAME": "marin-us-central2-vllm",
        "REGION": "us-central2",
        "ZONE": "us-central2-b",
        "BUCKET": "marin-us-central2",
        "DOCKER_TAG": "6e804a10",
        "tpu_generation": "v4-serve",
        "min_workers": 1,
        "VLLM": True,
    },
    "marin-us-east1-d-vllm": {
        "NAME": "marin-us-east1-d-vllm",
        "REGION": "us-east1",
        "ZONE": "us-east1-d",
        "BUCKET": "marin-us-east1",
        "DOCKER_TAG": "6e804a10",
        "tpu_generation": "v6e-serve",
        "min_workers": 2,
        "VLLM": True,
    },
}

generation_configs = {
    "v4": {
        "runtime_version": "tpu-ubuntu2204-base",
        "base_worker": "8",
        "slices": [16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
        "num_tpus": 4,
        "tpus_worker": 4,
    },
    "v5e": {
        "runtime_version": "v2-alpha-tpuv5-lite",
        "base_worker": "4",
        "slices": [8, 16, 32, 64, 128, 256],
        "num_tpus": 4,
        "tpus_worker": 1,
    },
    "v5p": {
        "runtime_version": "v2-alpha-tpuv5",
        "base_worker": "8",
        "slices": [8, 16, 32, 64, 128, 256, 512, 1024, 2048],
        "num_tpus": 4,
        "tpus_worker": 8,
    },
    "v6e": {
        "runtime_version": "v2-alpha-tpuv6e",
        "base_worker": "4",
        "slices": [8, 16, 32, 64, 128, 256],
        "num_tpus": 4,
    },
    "v6e-serve": {
        "runtime_version": "v2-alpha-tpuv6e",
        "base_worker": "8",
        "slices": [],
        "num_tpus": 8,
    },
    "v4-serve": {
        "runtime_version": "tpu-ubuntu2204-base",
        "base_worker": "16",
        "slices": [],
        "num_tpus": 4,
    },
}


def make_tpu_slice_config(generation, count, target_count) -> dict[str, dict]:
    slice_gen_name = "v5litepod" if generation == "v5e" else generation

    if "serve" in generation:
        slice_gen_name = generation.replace("-serve", "")
    name = f"tpu_slice_{generation}_{count}"
    return {
        name: {
            "min_workers": target_count,
            "max_workers": 1024,
            "resources": {"CPU": 120, "TPU": generation_configs[generation]["num_tpus"]},
            "node_config": {
                "acceleratorType": f"{slice_gen_name}-{count}",
                "runtimeVersion": generation_configs[generation]["runtime_version"],
                "schedulingConfig": {"preemptible": True},
            },
        }
    }


def get_template_path(config_name):
    if configs[config_name].get("VLLM", False):
        return vllm_template_path
    return cluster_template_path


def make_tpu_worker_config(generation, count, min_workers=4):
    _, config = next(iter(make_tpu_slice_config(generation, count, min_workers).items()))
    return {"tpu_worker": config}


if __name__ == "__main__":
    for config_name, config in configs.items():
        with open(os.path.join(this_path, f"{config_name}.yaml"), "w") as f:
            with open(get_template_path(config_name)) as f_template:
                template = jinja2.Template(f_template.read())

            yaml_string = template.render(**config)

            # pyyaml strips comments, which i'd like to keep
            # so instead of using yaml.dump, we'll write the string directly after appending worker types
            # (we need to indent it by 2 spaces)
            # available_node_types:
            generation = config["tpu_generation"]
            generation_config = generation_configs[generation]
            worker_config = make_tpu_worker_config(generation, generation_config["base_worker"], config["min_workers"])
            base_string = yaml.dump(worker_config, default_flow_style=False, indent=2)
            base_string = "\n  " + base_string.replace("\n", "\n  ")
            yaml_string += base_string

            for tpu_type in generation_config["slices"]:
                target_worker_count = config.get("worker_targets", {}).get(f"{generation}-{tpu_type}", 0)
                base_string = yaml.dump(
                    make_tpu_slice_config(generation, tpu_type, target_worker_count), default_flow_style=False, indent=2
                )
                base_string = "\n  " + base_string.replace("\n", "\n  ")
                yaml_string += base_string

            # Remove trailing whitespace from each line:
            lines = yaml_string.splitlines()
            lines = [line.rstrip() for line in lines]
            yaml_string = "\n".join(lines)

            f.write("#####################################################\n")
            f.write("#           THIS FILE IS AUTOGENERATED              #\n")
            f.write("# Update the template or the script, not this file! #\n")
            f.write("#####################################################\n")
            f.write(yaml_string)

            print(f"Generated {config_name} config")
