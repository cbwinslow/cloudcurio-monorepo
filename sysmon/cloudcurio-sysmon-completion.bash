#!/bin/bash
# bash completion for cloudcurio-sysmon

_cloudcurio_sysmon_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="setup snapshot list-snapshots reproduce events monitor --help --verbose"

    case "${prev}" in
        cloudcurio-sysmon)
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
            ;;
        events)
            local event_opts="--limit --type"
            COMPREPLY=( $(compgen -W "${event_opts}" -- ${cur}) )
            return 0
            ;;
        monitor)
            local monitor_opts="--continuous"
            COMPREPLY=( $(compgen -W "${monitor_opts}" -- ${cur}) )
            return 0
            ;;
        reproduce)
            # Complete snapshot names for the first argument after 'reproduce'
            if [[ $COMP_CWORD -eq 2 ]]; then
                local snapshots_dir="$HOME/.cloudcurio/snapshots"
                if [[ -d "$snapshots_dir" ]]; then
                    COMPREPLY=( $(compgen -W "$(ls $snapshots_dir)" -- ${cur}) )
                fi
            fi
            return 0
            ;;
    esac

    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "--help --verbose" -- ${cur}) )
        return 0
    fi
}

complete -F _cloudcurio_sysmon_completion cloudcurio-sysmon