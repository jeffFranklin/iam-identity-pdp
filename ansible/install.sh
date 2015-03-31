#!/bin/bash

# pdp ansible installation script

function usage {
  echo "usage: $0 [options] target "
  echo "       [-p playbook]  ( default: install.yml )"
  echo "       [-v]           ( verbose )"
  echo "       [-d]           ( very verbose )"
  echo "       [-i inventory] ( default:  ansible-tools/hosts )"
  echo "       [-q]           ( quick:  do not refresh ansible-toools )"
  echo "       targets: rivera_dev | rivera_prod"
  exit 1
}

# get the base path
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
base=${dir%/ansible}

cd $dir

target=
verbose=
quick=
list_opt=
playbook=install.yml

# generic parser
prefix=""
key=""
value=""
inventory=""
for keyValue in "$@"
do
  case "${prefix}${keyValue}" in
    -p=*|--playbook=*)  key="-p";     value="${keyValue#*=}";; 
    -i=*|--inventory=*)  key="-i";     value="${keyValue#*=}";; 
    -v*|--verbose)      key="-v";    value="";;
    -d*|--debug)      key="-d";    value="";;
    -q*|--quick)      key="-q";    value="";;
    -l*|--list)      key="-l";    value="";;
    -h*|-?|--help)             usage;;
    *)       value=$keyValue;;
  esac
  case $key in
    -p) playbook=${value}; echo "p=$playbook";  prefix=""; key="";;
    -i) inventory="${value}";          prefix=""; key="";;
    -v) verbose="-v";           prefix=""; key="";;
    -d) verbose="-vvvv";           prefix=""; key="";;
    -q) quick=q;           prefix=""; key="";;
    -l) list_opt="--list-hosts";           prefix=""; key="";;
    *)  prefix="${keyValue}=";;
  esac
done

[[ -z $target ]] && target=$value
[[ -z "$target"  || "$target" == "-"* ]] && usage

# get ansible-tools

[[ -d ansible-tools ]] || {
   echo "installing ansible-tools tools"
   git clone ssh://git@git.s.uw.edu/iam/ansible-tools.git
} || {
   [[ -z $quick ]] && {
      cd ansible-tools
      git pull origin master
      cd ..
   }
}

export ANSIBLE_LIBRARY=ansible-tools/modules:/usr/share/ansible

# store current status
cat > "install.status" << END
Personal preferences project (pdp) install

by: `whoami`
on: `date`

target: $target

branch:
`git branch -v| grep '^\*'`

status:
`git status -uno --porcelain`
END

# run the installer 

vars="target=${target} "
ansible-playbook ${playbook} $verbose  -i ansible-tools/hosts  --extra-vars "${vars}" $list_opt


