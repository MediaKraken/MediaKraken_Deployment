#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# this script downloads, verifies, and extracts archive files (.zip, .7z, .tar, .tar.gz, .tar.bz2) to the ut2004 folder

url=${1}            # argument 1, required, url of the archive
sha1=${2}           # argument 2, required, sha1 hash of downloaded file, used to verify file integrity
filename=${3}       # argument 3, required, filename of downloaded file
dest_dir=${4}       # argument 4, required, extract archive contents to this directory
src_dir=${5:-.}     # argument 5, optional, only extract this subdirectory from the archive

dir="/tmp/${RANDOM}"
download_file="${dir}/${filename}"
extract_dir="${dir}/extract"
tar_dir="${dir}/tar"
source_dir="${extract_dir}/${src_dir}/."

echo "Making temp directory ${extract_dir}"
mkdir --parents "${extract_dir}"

echo "Downloading ${url}"
curl --silent --show-error --location --output "${download_file}" "${url}"

echo "Verifying checksum ${sha1}"
echo "${sha1} ${download_file}" | sha1sum -c -

echo "Extracting to ${extract_dir}"
7z x -y "-o${extract_dir}" "${download_file}"

# check for single file as the output
extracted_files=$(ls -1 "${extract_dir}")
if [ "$(echo "${extracted_files}" | wc -l)" = "1" ]; then
  # check for tar file as the output
  if [ "$(echo "${extracted_files}" | grep \\.tar$ | wc -l)" = "1" ]; then
    echo "Inner tar detected"
    echo "Moving ${extract_dir} to ${tar_dir}"
    mv "${extract_dir}" "${tar_dir}"

    echo "Making temp directory ${extract_dir}"
    mkdir --parents "${extract_dir}"

    echo "Extracting to ${extract_dir}"
    7z x -y "-o${extract_dir}" "${tar_dir}/${extracted_files}"
  fi
fi

echo "Moving files from ${source_dir} to ${dest_dir}"
mkdir --parents ${dest_dir}
( cd "${source_dir}" && find . -type d -exec mkdir --parents "${dest_dir}/{}" \; )
( cd "${source_dir}" && find . -type f -exec mv {} "${dest_dir}/{}" \; )

echo "Cleanup ${dir}"
rm --recursive --force "${dir}"
