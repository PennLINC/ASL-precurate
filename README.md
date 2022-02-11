# ASL-precurate
A tool to extract and parse ASL dicom headers before BIDS curation

Usage:

```
usage: asl-precurate [-h] --container CONTAINER [--use-tmpdir | --use-cwd] dicom_dir

asl-precurate: Extract and Parse ASL DICOM Headers

positional arguments:
  dicom_dir             Path to DICOM ZIP file

optional arguments:
  -h, --help            show this help message and exit
  --container CONTAINER
                        Docker image tag or Singularity image file. (default: None)
  --use-tmpdir          Use Python's tmpdir pkg to unzip the DICOM (default: True)
  --use-cwd             Use the current working directory to unzip the DICOM (default: True)
  ```

0. Clone this repo and install with `pip`

```
git clone https://github.com/PennLINC/ASL-precurate.git
cd ASL-precurate
pip install -e .
```

1. Download a valid ASL DICOM file (must be a zipped DICOM -- no need to extract)

2. Grab the docker image from dockerhub

```
docker pull pennlinc/asl-precurate:latest
```

3. Run `asl-precurate /PATH/TO/dicom.zip --container pennlinc/asl-precurate:latest --use-tmpdir`

4. [Optional] Pipe your output to a text file to make it easy to share
```
`asl-precurate /PATH/TO/dicom.zip --container pennlinc/asl-precurate:latest --use-tmpdir > /PATH/TO/AN/OUTPUT/file.txt` 
```
