#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

neofetch

export PATH=$PATH:$HOME/mysql/mysql-8.3.0-linux-glibc2.28-x86_64/bin

eval "$(starship init bash)"
