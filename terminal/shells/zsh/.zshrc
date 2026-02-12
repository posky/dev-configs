# =========================
# 기본: 히스토리 / 옵션
# =========================
HISTFILE="$HOME/.zsh_history"
HISTSIZE=100000
SAVEHIST=100000

setopt HIST_IGNORE_DUPS        # 연속 중복 기록 제거
setopt HIST_IGNORE_SPACE       # 앞에 공백 있는 명령은 기록 안 함
setopt HIST_SAVE_NO_DUPS        # 파일 저장 시에도 중복 제거
setopt HIST_REDUCE_BLANKS       # 불필요 공백 줄이기
setopt HIST_EXPIRE_DUPS_FIRST   # 히스토리 넘칠 때 중복부터 삭제
setopt HIST_VERIFY             # !! 등의 확장 결과를 실행 전 보여줌
setopt SHARE_HISTORY           # 여러 세션에서 히스토리 공유(취향)
setopt INC_APPEND_HISTORY      # 실행 즉시 히스토리 파일에 반영
setopt HIST_FCNTL_LOCK
setopt EXTENDED_HISTORY        # 타임스탬프 포함

unsetopt AUTO_CD                 # 디렉터리명만 쳐도 cd
setopt AUTO_PUSHD              # cd 시 pushd 처럼 동작(취향)
setopt PUSHD_IGNORE_DUPS
setopt PUSHD_SILENT
DIRSTACKSIZE=20
setopt NO_BEEP


# =========================
# 키바인딩 / 편의
# =========================
bindkey -v                      # vi 키바인딩
KEYTIMEOUT=1   # ESC 지연 줄여서 vi 모드 반응 개선


# =========================
# env
# =========================

export PATH="$HOME/.local/bin:$PATH"

[[ -f "$HOME/.local/bin/env" ]] && source "$HOME/.local/bin/env" 2>/dev/null || true

export LANG=en_US.UTF-8

if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env --use-on-cd --shell zsh --corepack-enabled)"
fi

# psql (postgresql)
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"



# =========================
# Completions dir
# =========================
ZSH_COMPLETIONS_DIR="$HOME/.local/share/zsh/completions"
mkdir -p "$ZSH_COMPLETIONS_DIR"

fpath=("$ZSH_COMPLETIONS_DIR" $fpath)
fpath=("$HOME/.local/src/eza/completions/zsh" $fpath)

if command -v uv >/dev/null 2>&1 && [[ ! -s "$ZSH_COMPLETIONS_DIR/_uv" ]]; then
  uv generate-shell-completion zsh >| "$ZSH_COMPLETIONS_DIR/_uv"
fi
if command -v uvx >/dev/null 2>&1 && [[ ! -s "$ZSH_COMPLETIONS_DIR/_uvx" ]]; then
  uvx --generate-shell-completion zsh >| "$ZSH_COMPLETIONS_DIR/_uvx"
fi
if command -v fnm >/dev/null 2>&1 && [[ ! -s "$ZSH_COMPLETIONS_DIR/_fnm" ]]; then
  fnm completions --shell zsh >| "$ZSH_COMPLETIONS_DIR/_fnm"
fi
if command -v but >/dev/null 2>&1 && [[ ! -s "$ZSH_COMPLETIONS_DIR/_but" ]]; then
  but completions zsh >| "$ZSH_COMPLETIONS_DIR/_but"
fi


### Added by Zinit's installer
if [[ ! -f $HOME/.local/share/zinit/zinit.git/zinit.zsh ]]; then
    print -P "%F{33} %F{220}Installing %F{33}ZDHARMA-CONTINUUM%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
    command mkdir -p "$HOME/.local/share/zinit" && command chmod g-rwX "$HOME/.local/share/zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.local/share/zinit/zinit.git" && \
        print -P "%F{33} %F{34}Installation successful.%f%b" || \
        print -P "%F{160} The clone has failed.%f%b"
fi

source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
# autoload -Uz _zinit
# (( ${+_comps} )) && _comps[zinit]=_zinit

# Load a few important annexes, without Turbo
# (this is currently required for annexes)
zinit light-mode for \
    zdharma-continuum/zinit-annex-as-monitor \
    zdharma-continuum/zinit-annex-bin-gem-node \
    zdharma-continuum/zinit-annex-patch-dl \
    zdharma-continuum/zinit-annex-rust

### End of Zinit's installer chunk


# zsh-autocomplete (must be before compdef)
zinit light marlonrichert/zsh-autocomplete
zstyle ':autocomplete:*' delay 0.2
zstyle ':autocomplete:*' timeout 1.0
zstyle ':autocomplete:*' append-semicolon no
zstyle ':autocomplete:*' min-input 2
zstyle ':autocomplete:*complete*:*' insert-unambiguous yes
zstyle ':autocomplete:*history*:*' insert-unambiguous yes


# =========================
# Alias / 기본 유틸
# =========================
alias ll='ls -alh'
alias la='ls -A'
if command -v eza >/dev/null 2>&1; then
  alias ls='eza'
  alias ll='eza -lah --group-directories-first --icons'
  alias la='eza -a --icons'
fi
alias vim=nvim

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'
else
  export EDITOR='nvim'
fi

function macUpdate() {
  if [ -f ~/.local/bin/update ]; then
    ~/.local/bin/update
  fi
}

# tmux attach with list
ta() {
  if ! command -v tmux &>/dev/null; then
    echo "tmux not installed"; return 1
  fi

  # tmux 서버 자체가 없으면 새로 생성
  if ! tmux ls &>/dev/null; then
    tmux new-session -s main
    return
  fi

  local session
  session=$(tmux ls -F "#{session_name}" | fzf --prompt="tmux session > ")
  [[ -n "$session" ]] || return

  if [[ -n "$TMUX" ]]; then
    tmux switch-client -t "$session"
  else
    tmux attach -t "$session"
  fi
}


# =========================
# fastfetch
# =========================
case $- in
  *i*) command -v fastfetch >/dev/null 2>&1 && fastfetch ;;
esac

# =========================
# starship
# =========================
case $- in
  *i*) eval "$(starship init zsh)" ;;
esac

# zsh-syntax-highlighting
zinit light zsh-users/zsh-syntax-highlighting
