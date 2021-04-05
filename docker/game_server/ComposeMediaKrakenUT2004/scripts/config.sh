#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# modify ini files
for i in `seq 1 100`; do
    eval modify=\${CONFIG_${i}:-}
    if [ -z "$modify" ]; then continue; fi

    echo "Processing CONFIG_${i}"

    eval file=\${CONFIG_${i}_FILE:-UT2004.ini}
    eval delimit=\${CONFIG_${i}_DELIMIT:-}

    output="${UT2004_HOME}/.ut2004/System/${file}"

    if [ -f "${output}" ]; then
      input="${output}"
    elif [ -f "${UT2004_DIR}/System/${file}" ]; then
      input="${UT2004_DIR}/System/${file}"
    else
      input=""
    fi

    echo "input file: ${input}  output file: ${output}"
    modini --input "${input}" --output "${output}" --modify "${modify}" --delimit "${delimit:-;}"
done
