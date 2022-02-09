import os
import logging
import subprocess
import argparse
import subprocess
import re
import tempfile
from pathlib import Path
from zipfile import ZipFile


logger = logging.getLogger("Precurate")
logging.basicConfig(level=logging.INFO)


def build_call(opts):
    '''
    Build the ultimate docker call string

    example usage:

    docker run --rm -ti \ 
        -v /Users/ttapera/Downloads/asl.dicom/1.3.12.2.1107.5.2.32.35069.2013072909575233959525730.MR.dcm:/mnt/inputs/input.dcm \
        pennlinc/asl-precurate:latest \
        -i /mnt/inputs/input.dcm
    '''

    container_type = _get_container_type(opts.container)
    dicom_dir_link = "{}:/inputs/dicom.dcm"
    
    if container_type == 'docker':
        cmd = ['docker', 'run', '--rm', '-v', dicom_dir_link,
               '--entrypoint', 'gdcmdump',
               opts.container, '/inputs/dicom.dcm', '--csa']
    
    elif container_type == 'singularity':
        cmd = ['singularity', 'exec', '--cleanenv',
               '-B', dicom_dir_link,
               opts.container, 'gdcmdump',
               '/inputs/dicom.dcm', '--csa']
    
    return cmd


def run_call_with_container(call, opts):
    '''Run the call to the container'''

    if opts.tmpdir:

        with tempfile.TemporaryDirectory() as tempdir:

            with ZipFile(opts.dicom_dir, 'r') as zipObject:
                file_names = zipObject.namelist()

                full_path = tempdir + "/" + file_names[0]
                
                zipObject.extract(file_names[0], tempdir)
                
                call = ' '.join(call).format(full_path)
                logger.info("\tRunning Container Call:\n\n" + call)

                ret = subprocess.run(call.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                parse_return(ret)

    else:

        with ZipFile(opts.dicom_dir, 'r') as zipObject:

            file_names = zipObject.namelist()

            full_path = str(opts.dicom_dir).replace(".zip", "") + "/" + file_names[0]
            
            zipObject.extract(file_names[0])
            call = ' '.join(call).format(full_path).format(full_path)
            logger.info("\tRunning Container Call:\n\n" + call)

            ret = subprocess.run(call.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(ret)
            parse_return(ret)


def parse_return(subp):

    if subp.returncode != 0:
        logger.error("Errors returned from container command, parsing now")
        print(subp.stdout.decode('UTF-8'))
        raise RuntimeError
    
    print(subp.stdout.decode('UTF-8'))


def parse_arguments():
    
    parser = argparse.ArgumentParser(
        description="asl-precurate: Extract and Parse ASL DICOM "
        "Headers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dicom_dir',
                        type=Path,
                        action='store',
                        help='Path to DICOM ZIP file'
                        )
    parser.add_argument('--container',
                        action='store',
                        help='Docker image tag or Singularity image file.',
                        required=True
                        )

    tmpdir_parser = parser.add_mutually_exclusive_group(required=False)
    tmpdir_parser.add_argument('--use-tmpdir',
                        dest="tmpdir",
                        action='store_true',
                        help="Use Python's tmpdir pkg to unzip the DICOM",
                        )
    tmpdir_parser.add_argument('--use-cwd',
                        dest="tmpdir",
                        action='store_false',
                        help="Use the current working directory to unzip the DICOM",
                        )
    parser.set_defaults(tmpdir=True)

    opts = parser.parse_args()
    logger.debug(opts)

    assert _is_valid_zipfile(opts.dicom_dir), "Ensure that this is a valid DICOM Zipfile"
    return opts


def _get_container_type(image_name):
    '''Gets and returns the container type.'''

    # If it's a file on disk, it must be a singularity image
    if Path(image_name).exists():
        return "singularity"

    # It needs to match a docker tag pattern to be docker
    if re.match(r"(?:.+\/)?([^:]+)(?::.+)?", image_name):
        return "docker"

    raise Exception("Unable to determine the container type of "
                    + image_name)


def _is_valid_zipfile(input_file):
    '''Ensures that the input data is a valid zipfile'''

    logger.debug("Validating File {}".format(input_file))
    
    f_exists = Path(input_file).is_file()
    
    try:
        with ZipFile(input_file, 'r') as zipObject:
            file_names = zipObject.namelist()
            logger.debug("{} dicom ZIP members".format(len(file_names)))
            
            f_is_zip = True
    except:
        logger.exception("Not a valid ZIP file")
        f_is_zip = False

    return all([f_exists, f_is_zip])

def main():

    opts = parse_arguments()
    cmd = build_call(opts)
    #logger.info(' '.join(cmd))

    run_call_with_container(cmd, opts)

main()