# The following lines were added by compinstall

zstyle ':completion:*' completer _complete _ignored _approximate
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' matcher-list 'm:{[:lower:]}={[:upper:]}' 'm:{[:lower:]}={[:upper:]}' 'm:{[:lower:]}={[:upper:]}' 'm:{[:lower:]}={[:upper:]}'
zstyle :compinstall filename '/home/juntunenkc/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
# bindkey -v
# bindkey '^R' history-incremental-search-backward
# End of lines configured by zsh-newuser-install
#
EDITOR=/home/juntunenkc/bin/em

bindkey -v

bindkey '^P' up-history
bindkey '^N' down-history
bindkey '^?' backward-delete-char
bindkey '^h' backward-delete-char
bindkey '^w' backward-kill-word
bindkey '^r' history-incremental-search-backward
export KEYTIMEOUT=1

#function zle-line-init zle-keymap-select {
#    RPS1="${${KEYMAP/vicmd/-- NORMAL --}/(main|viins)/-- INSERT --}"
#    RPS2=$RPS1
#    zle reset-prompt
#}
#
#zle -N zle-line-init
#zle -N zle-keymap-select
. ~/git/spaceship-prompt/spaceship.zsh

alias wanip='dig +short myip.opendns.com @resolver1.opendns.com '

export SSH_AGENT_PID=$(pgrep ssh-agent)
if [ $SSH_AGENT_PID ]; then
	export SSH_AUTH_SOCK=$(find /tmp/ -name "agent.*" 2&>/dev/null)
  echo "SSH Agent already running. PID: $SSH_AGENT_PID"
  echo "SSH Agent auth sock: $SSH_AUTH_SOCK"
else
  eval $(ssh-agent)
	ssh-add ~/.ssh/id*
fi

