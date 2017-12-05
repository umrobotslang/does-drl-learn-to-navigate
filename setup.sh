CURRDIR=$(dirname $(readlink -m "${BASH_SOURCE[0]}"))
PS1=(drl-nav).$PS1
echo "Appending (drl-nav) to PS1"
if [ ! "${INSTALL_PREFIX}" ]; then
    INSTALL_PREFIX="${CURRDIR}/build"
    echo "setting INSTALL_PREFIX to ${INSTALL_PREFIX}"
fi
export LC_ALL="C"
source ${INSTALL_PREFIX}/etc/profile.d/modules.sh
module use ${CURRDIR}/deepmind-lab/envmodule/
module load deepmind-lab.mod
module use ${CURRDIR}/modules
module load implicit-mapping.mod
alias jobstat="qstat -tfu $USER | grep -E 'Job( Id|_Name)|PBS_O_WORKDIR|exec_host|job_state'"
