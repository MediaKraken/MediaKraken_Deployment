#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# check for additional downloads
for i in `seq 1 100`; do
    eval url=\${DOWNLOAD_${i}_URL:-}
    if [ -z "$url" ]; then continue; fi

    echo "Processing DOWNLOAD_${i}"

    eval sha1=\${DOWNLOAD_${i}_SHA1}
    eval file=\${DOWNLOAD_${i}_FILE}
    eval dest_dir=\${DOWNLOAD_${i}_DEST_DIR:-.}
    eval src_dir=\${DOWNLOAD_${i}_SRC_DIR:-.}

    if [ -f "${UT2004_HOME}/.ut2004/downloads/${sha1}" ]; then
        echo "Download #${i} already installed: ${file}"
    else
        install.sh "${url}" "${sha1}" "${file}" "${UT2004_HOME}/.ut2004/${dest_dir}" "${src_dir}"
        mkdir -p "${UT2004_HOME}/.ut2004/downloads"
        touch "${UT2004_HOME}/.ut2004/downloads/${sha1}"
    fi
done
