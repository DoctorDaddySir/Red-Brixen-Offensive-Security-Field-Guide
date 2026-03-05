#!/usr/bin/env bash
# This script is a simple engagement companion designed to help you stay on task under tight time constraints.     #
# It provides a menu of timed stages you can run throughout an exam-style session, automatically schedules breaks  #
# and naps, and prompts you to confirm documentation after key steps. It also includes a built-in score tracker    #
# aligned to OSCP+ style objectives and clearly indicates when you’ve reached a passing threshold.                 #
#                                                                                                DoctorDaddySir    #

set -uo pipefail

PASSING_SCORE_THRESHOLD=70

STANDALONE_INITIAL_ACCESS_POINTS=10
STANDALONE_PRIVESC_POINTS=10
AD_MACHINE_ONE_POINTS=10
AD_MACHINE_TWO_POINTS=10
AD_DOMAIN_CONTROLLER_POINTS=20

score_log_file_path="score_log.txt"

break_interval_seconds=$((90*60))
reassessment_interval_seconds=$((3*60*60))
break_duration_seconds=$((5*60))
reassessment_duration_seconds=$((2*60))

nap_duration_seconds=$((120*60))
nap_offset_schedule=( $((6*60*60)) $((14*60*60)) $((22*60*60)) )

documentation_sprint_minutes=15

EXIT_PHRASE="EXIT"

controlling_terminal="/dev/tty"

terminal_rows=24
terminal_columns=80
status_bar_row=24
command_input_row=23

current_ui_mode="MENU"
current_stage_name="menu"
current_stage_seconds_remaining=-1
ui_input_mode_active=0

last_rendered_status_snapshot=""

exam_start_epoch=0
exam_end_epoch=0

next_break_epoch=0
next_reassessment_epoch=0
scheduled_nap_epochs=()
next_nap_index=0

declare -A score_registry 2>/dev/null || true
current_total_score=0
current_standalone_score=0
current_active_directory_score=0

stage_cancel_requested=0
forced_interrupt=0

ansi_reset=$'\033[0m'

ansi_mode_segment=$'\033[97;48;5;240m'
ansi_remaining_segment=$'\033[30;48;5;214m'
ansi_stage_remaining_segment=$'\033[30;48;5;229m'
ansi_break_segment=$'\033[97;48;5;141m'
ansi_reassessment_segment=$'\033[97;48;5;27m'
ansi_nap_segment=$'\033[30;48;5;120m'

ansi_standalone_score_segment=$'\033[97;48;5;160m'
ansi_ad_score_segment=$'\033[97;48;5;90m'
ansi_total_score_pass_segment=$'\033[30;48;5;82m'
ansi_total_score_fail_segment=$'\033[97;48;5;196m'

saved_stty_state=""

save_tty_state() {
  saved_stty_state="$(stty -g <"$controlling_terminal" 2>/dev/null || true)"
}

restore_tty_state() {
  [[ -n "${saved_stty_state:-}" ]] && stty "$saved_stty_state" <"$controlling_terminal" 2>/dev/null || true
}

set_raw_keys_mode() {
  save_tty_state
  stty -icanon -echo min 0 time 0 <"$controlling_terminal" 2>/dev/null || true
}

cleanup() {
  restore_tty_state
  printf "\033[?25h\033[0m\n" >"$controlling_terminal" 2>/dev/null || true
}

trap cleanup EXIT
trap 'printf "\nCtrl-C blocked. Use Exit option.\n" >"$controlling_terminal"; sleep 1' INT TERM QUIT

update_terminal_size() {
  local r c
  r="$(tput lines 2>/dev/null || echo 24)"
  c="$(tput cols 2>/dev/null || echo 80)"
  [[ "$r" =~ ^[0-9]+$ ]] && terminal_rows="$r" || terminal_rows=24
  [[ "$c" =~ ^[0-9]+$ ]] && terminal_columns="$c" || terminal_columns=80
  (( terminal_rows < 10 )) && terminal_rows=24
  (( terminal_columns < 40 )) && terminal_columns=80
  status_bar_row="$terminal_rows"
  command_input_row=$((terminal_rows-1))
  (( command_input_row < 1 )) && command_input_row=1
}

trap 'update_terminal_size' WINCH

cup() { printf "\033[%d;%dH" "$1" "$2" >"$controlling_terminal"; }
clear_line() { printf "\033[2K" >"$controlling_terminal"; }
clear_screen() { printf "\033[2J\033[H" >"$controlling_terminal"; }
hide_cursor() { printf "\033[?25l" >"$controlling_terminal"; }
show_cursor() { printf "\033[?25h" >"$controlling_terminal"; }
beep() { printf "\a" >"$controlling_terminal" 2>/dev/null || true; }

format_time_hms() {
  local t="${1:-0}"
  [[ "$t" =~ ^-?[0-9]+$ ]] || t=0
  (( t < 0 )) && t=0
  printf "%02d:%02d:%02d" $((t/3600)) $(((t%3600)/60)) $((t%60))
}

format_epoch_hm() {
  local e="$1"
  date -d "@$e" +"%H:%M" 2>/dev/null || date +"%H:%M"
}

strip_ansi() { sed -r 's/\x1B\[[0-9;]*[A-Za-z]//g'; }

segment() {
  local color="$1" text="$2"
  printf "%s %s %s" "$color" "$text" "$ansi_reset"
}

poll_key_1s_raw() {
  local k=""
  for _ in {1..10}; do
    IFS= read -rsn1 -t 0.1 k <"$controlling_terminal" 2>/dev/null || true
    [[ -n "$k" ]] && break
  done
  printf "%s" "$k"
}

recompute_scores() {
  current_total_score=0
  current_standalone_score=0
  current_active_directory_score=0

  local key points
  for key in "${!score_registry[@]}"; do
    points="${score_registry[$key]}"
    [[ "$points" =~ ^[0-9]+$ ]] || points=0
    (( current_total_score += points ))
    case "$key" in
      AD1|AD2|DC) (( current_active_directory_score += points )) ;;
      SA*)        (( current_standalone_score += points )) ;;
    esac
  done
}

log_score_entry() {
  printf "%s | %s\n" "$(date '+%F %T')" "$1" >> "$score_log_file_path"
}

pass_indicator() {
  (( current_total_score >= PASSING_SCORE_THRESHOLD )) && echo "PASS" || echo "NOPASS"
}

calc_left() {
  local now remaining b r n
  now="$(date +%s)"

  remaining=$((exam_end_epoch - now))
  (( remaining < 0 )) && remaining=0

  b=$((next_break_epoch - now)); (( b < 0 )) && b=0
  r=$((next_reassessment_epoch - now)); (( r < 0 )) && r=0

  n=-1
  if (( next_nap_index < ${#scheduled_nap_epochs[@]} )); then
    n=$(( ${scheduled_nap_epochs[$next_nap_index]} - now ))
    (( n < 0 )) && n=0
  fi

  printf "%s %s %s %s %s\n" "$now" "$remaining" "$b" "$r" "$n"
}

render_status_line() {
  local now remaining b r n
  read -r now remaining b r n < <(calc_left)

  local nap_display="--:--:--"
  (( n >= 0 )) && nap_display="$(format_time_hms "$n")"

  local stage_display="--:--:--"
  (( current_stage_seconds_remaining >= 0 )) && stage_display="$(format_time_hms "$current_stage_seconds_remaining")"

  local total_color="$ansi_total_score_fail_segment"
  (( current_total_score >= PASSING_SCORE_THRESHOLD )) && total_color="$ansi_total_score_pass_segment"

  printf "%s%s%s%s%s%s%s%s%s%s%s%s" \
    "$(segment "$ansi_mode_segment" "MODE:$current_ui_mode")" \
    "$(segment "$ansi_remaining_segment" "REM:$(format_time_hms "$remaining")")" \
    "$(segment "$ansi_mode_segment" "STG:$current_stage_name")" \
    "$(segment "$ansi_stage_remaining_segment" "LEFT:$stage_display")" \
    "$(segment "$ansi_break_segment" "BRK:$(format_time_hms "$b")")" \
    "$(segment "$ansi_reassessment_segment" "RST:$(format_time_hms "$r")")" \
    "$(segment "$ansi_nap_segment" "NAP:$nap_display")" \
    "$(segment "$ansi_standalone_score_segment" "SA:${current_standalone_score}/60")" \
    "$(segment "$ansi_ad_score_segment" "AD:${current_active_directory_score}/40")" \
    "$(segment "$total_color" "TOT:${current_total_score}/100")" \
    "$(segment "$total_color" "$(pass_indicator)")" \
    "$(segment "$ansi_mode_segment" "?=help")"
}

draw_status_bar() {
  (( ui_input_mode_active == 1 )) && return 0

  local rendered plain pad
  rendered="$(render_status_line)"
  plain="$(printf "%s" "$rendered" | strip_ansi)"

  [[ "$plain" == "$last_rendered_status_snapshot" ]] && return 0
  last_rendered_status_snapshot="$plain"

  pad=$((terminal_columns - ${#plain}))
  (( pad < 0 )) && pad=0

  printf "\0337" >"$controlling_terminal"
  cup "$status_bar_row" 1
  printf "%s%*s%s" "$rendered" "$pad" "" "$ansi_reset" >"$controlling_terminal"
  printf "\0338" >"$controlling_terminal"
}

clear_content_area() {
  local r
  for ((r=1; r<=command_input_row-1; r++)); do
    cup "$r" 1
    clear_line
  done
}

print_menu() {
  clear_content_area
  cup 1 1

  local start_hm end_hm
  start_hm="$(format_epoch_hm "$exam_start_epoch")"
  end_hm="$(format_epoch_hm "$exam_end_epoch")"

  cat >"$controlling_terminal" <<EOF
========== OSCP+ ENGAGEMENT GOVERNOR ==========
Start: $start_hm    End: $end_hm  (23h45m)

1) Recon (25m)
2) Exploitation Attempt (45m)
3) Linux PrivEsc Funnel (20m)
4) Windows PrivEsc Funnel (30m)
5) Gap Review (10m)
6) Documentation Sprint (15m)
7) Manual Break (5m)
8) Manual Nap (120m)
9) Score Entry
?) Help
0) Exit

EOF
  draw_status_bar
}

print_help() {
  clear_content_area
  cup 1 1
  cat >"$controlling_terminal" <<EOF
HELP

- Select a stage from the menu to start a timer.
- During stages that allow it, press 'e' to end early.
- Breaks and naps are scheduled and will take priority.
- Score Entry records OSCP+ objectives (no duplicates).
- Exit requires typing the confirmation phrase.

EOF
  draw_status_bar
}

prompt_line_with_ticking_status() {
  local prompt="$1"
  local line=""

  forced_interrupt=0

  printf "\0337" >"$controlling_terminal"
  cup "$command_input_row" 1
  clear_line
  printf "%s" "$prompt" >"$controlling_terminal"
  printf "\0338" >"$controlling_terminal"

  show_cursor
  while true; do
    check_and_enforce && { forced_interrupt=1; line=""; break; }
    draw_status_bar
    if IFS= read -r -t 1 line <"$controlling_terminal"; then
      break
    fi
  done
  hide_cursor
  printf "%s" "$line"
}

shift_schedules_forward() {
  local delta="$1"
  (( delta <= 0 )) && return 0

  exam_start_epoch=$((exam_start_epoch + delta))
  exam_end_epoch=$((exam_end_epoch + delta))
  next_break_epoch=$((next_break_epoch + delta))
  next_reassessment_epoch=$((next_reassessment_epoch + delta))

  local i
  for i in "${!scheduled_nap_epochs[@]}"; do
    if (( i >= next_nap_index )); then
      scheduled_nap_epochs[$i]=$((scheduled_nap_epochs[$i] + delta))
    fi
  done
}

enforce_reassessment() {
  current_ui_mode="RST"
  current_stage_name="reassess_due"
  last_rendered_status_snapshot=""
  clear_content_area
  cup 1 1
  printf "RST DUE NOW\n\n" >"$controlling_terminal"
  printf "Immediate check: are you working on the right things?\n" >"$controlling_terminal"
  printf "y = continue, n = change focus (stage cancels)\n\n" >"$controlling_terminal"
  draw_status_bar

  local ans
  ans="$(prompt_line_with_ticking_status "Right objective? (y/n): ")"
  [[ $forced_interrupt -eq 1 ]] && return 0

  case "${ans,,}" in
    y|yes)
      current_stage_seconds_remaining="$reassessment_duration_seconds"
      while (( current_stage_seconds_remaining > 0 )); do
        draw_status_bar
        sleep 1
        ((current_stage_seconds_remaining--))
      done
      current_stage_seconds_remaining=0
      draw_status_bar
      beep
      local now; now="$(date +%s)"
      next_reassessment_epoch=$((now + reassessment_interval_seconds))
      ;;
    n|no)
      clear_content_area
      cup 1 1
      printf "CHANGE NEEDED\n\n" >"$controlling_terminal"
      printf "Document current status FIRST (what tested / result / next hypothesis).\n" >"$controlling_terminal"
      printf "Then switch deliberately.\n\n" >"$controlling_terminal"
      draw_status_bar
      prompt_line_with_ticking_status "Press ENTER when documentation is done... " >/dev/null

      stage_cancel_requested=1
      local now2; now2="$(date +%s)"
      next_reassessment_epoch=$((now2 + reassessment_interval_seconds))
      ;;
    *)
      local now3; now3="$(date +%s)"
      next_reassessment_epoch=$((now3 + reassessment_interval_seconds))
      ;;
  esac
}

enforce_nap() {
  current_ui_mode="NAP"
  current_stage_name="nap"
  current_stage_seconds_remaining="$nap_duration_seconds"
  last_rendered_status_snapshot=""

  while (( current_stage_seconds_remaining > 0 )) ; do
    draw_status_bar
    sleep 1
    ((current_stage_seconds_remaining--))
  done

  current_stage_seconds_remaining=0
  draw_status_bar
  beep
  ((next_nap_index++))
}

enforce_break_pause_all() {
  current_ui_mode="BRK"
  current_stage_name="break_due"
  last_rendered_status_snapshot=""

  clear_content_area
  cup 1 1
  printf "BREAK DUE NOW\n\n" >"$controlling_terminal"
  printf "b = take break now (full duration)\n" >"$controlling_terminal"
  printf "p = postpone 10 minutes\n\n" >"$controlling_terminal"
  draw_status_bar

  local choice
  choice="$(prompt_line_with_ticking_status "Choice (b/p): ")"
  [[ $forced_interrupt -eq 1 ]] && return 0

  case "${choice,,}" in
    p)
      next_break_epoch=$((next_break_epoch + 600))
      clear_content_area
      cup 1 1
      printf "Break postponed by 10 minutes.\n\n" >"$controlling_terminal"
      draw_status_bar
      sleep 1
      return 0
      ;;
    b|*)
      ;;
  esac

  current_ui_mode="BREAK"
  current_stage_name="break"
  last_rendered_status_snapshot=""

  local start_wall end_wall actual
  start_wall="$(date +%s)"

  current_stage_seconds_remaining="$break_duration_seconds"
  while (( current_stage_seconds_remaining > 0 )); do
    draw_status_bar
    sleep 1
    ((current_stage_seconds_remaining--))
  done

  current_stage_seconds_remaining=0
  draw_status_bar
  beep

  end_wall="$(date +%s)"
  actual=$((end_wall - start_wall))
  (( actual < 0 )) && actual=0

  shift_schedules_forward "$actual"
  next_break_epoch=$((end_wall + break_interval_seconds))
}

check_and_enforce() {
  local now; now="$(date +%s)"

  if (( next_nap_index < ${#scheduled_nap_epochs[@]} )) && (( now >= ${scheduled_nap_epochs[$next_nap_index]} )); then
    enforce_nap; return 0
  fi

  if (( now >= next_reassessment_epoch )); then
    enforce_reassessment; return 0
  fi

  if (( now >= next_break_epoch )); then
    enforce_break_pause_all; return 0
  fi

  return 1
}

run_stage() {
  local label="$1" minutes="$2" allow_early="$3"

  stage_cancel_requested=0
  current_ui_mode="STAGE"
  current_stage_name="$label"
  current_stage_seconds_remaining=$((minutes*60))
  last_rendered_status_snapshot=""

  clear_content_area
  cup 1 1
  printf "STAGE: %s\n" "$label" >"$controlling_terminal"
  if (( allow_early == 1 )); then
    printf "Press 'e' to end early. '?' for help.\n\n" >"$controlling_terminal"
  else
    printf "Press '?' for help.\n\n" >"$controlling_terminal"
  fi

  set_raw_keys_mode
  hide_cursor

  while (( current_stage_seconds_remaining > 0 )); do
    check_and_enforce || true
    if (( stage_cancel_requested == 1 )); then
      break
    fi

    draw_status_bar
    local k; k="$(poll_key_1s_raw)"
    if [[ -n "$k" ]]; then
      case "$k" in
        \?)
          restore_tty_state; show_cursor
          print_help
          prompt_line_with_ticking_status "Press ENTER... " >/dev/null
          clear_content_area
          cup 1 1
          printf "STAGE: %s\n" "$label" >"$controlling_terminal"
          set_raw_keys_mode; hide_cursor
          ;;
        e|E)
          if (( allow_early == 1 )); then
            break
          fi
          ;;
      esac
    else
      ((current_stage_seconds_remaining--))
    fi
  done

  restore_tty_state
  show_cursor

  if (( stage_cancel_requested == 1 )); then
    current_ui_mode="MENU"
    current_stage_name="menu"
    current_stage_seconds_remaining=-1
    last_rendered_status_snapshot=""
    beep
    return 0
  fi

  current_stage_seconds_remaining=0
  draw_status_bar
  beep
}

doc_checkpoint_loop() {
  local stage_label="$1"
  while true; do
    local ans; ans="$(prompt_line_with_ticking_status "Docs complete for '$stage_label'? (y/n): ")"
    [[ $forced_interrupt -eq 1 ]] && return 0
    case "${ans,,}" in
      y|yes) return 0 ;;
      n|no)  run_stage "Documentation Sprint" "$documentation_sprint_minutes" 1 || true ;;
      *) ;;
    esac
  done
}

score_menu() {
  while true; do
    clear_content_area
    cup 1 1
    cat >"$controlling_terminal" <<EOF
SCORE ENTRY

Standalone:
  1) SA1 IA (+10)
  2) SA1 PE (+10)
  3) SA2 IA (+10)
  4) SA2 PE (+10)
  5) SA3 IA (+10)
  6) SA3 PE (+10)

Active Directory:
  7) AD1 (+10)
  8) AD2 (+10)
  9) DC  (+20)

Other:
  r) Remove recorded item
  b) Back

EOF
    draw_status_bar

    local choice; choice="$(prompt_line_with_ticking_status "CMD> ")"
    [[ $forced_interrupt -eq 1 ]] && { last_rendered_status_snapshot=""; continue; }

    local key="" pts=0

    case "${choice,,}" in
      1) key="SA1_IA"; pts=$STANDALONE_INITIAL_ACCESS_POINTS ;;
      2) key="SA1_PE"; pts=$STANDALONE_PRIVESC_POINTS ;;
      3) key="SA2_IA"; pts=$STANDALONE_INITIAL_ACCESS_POINTS ;;
      4) key="SA2_PE"; pts=$STANDALONE_PRIVESC_POINTS ;;
      5) key="SA3_IA"; pts=$STANDALONE_INITIAL_ACCESS_POINTS ;;
      6) key="SA3_PE"; pts=$STANDALONE_PRIVESC_POINTS ;;
      7) key="AD1";    pts=$AD_MACHINE_ONE_POINTS ;;
      8) key="AD2";    pts=$AD_MACHINE_TWO_POINTS ;;
      9) key="DC";     pts=$AD_DOMAIN_CONTROLLER_POINTS ;;
      b) return 0 ;;
      r)
        local rkey; rkey="$(prompt_line_with_ticking_status "Remove key (SA2_PE, DC) or blank: ")"
        rkey="${rkey^^}"
        if [[ -n "$rkey" && -n "${score_registry[$rkey]+x}" ]]; then
          unset 'score_registry[$rkey]'
          recompute_scores
          prompt_line_with_ticking_status "Removed $rkey. Press ENTER... " >/dev/null
        else
          prompt_line_with_ticking_status "No change. Press ENTER... " >/dev/null
        fi
        continue
        ;;
      *) continue ;;
    esac

    if [[ -n "${score_registry[$key]+x}" ]]; then
      prompt_line_with_ticking_status "Already recorded $key. Press ENTER... " >/dev/null
      continue
    fi

    score_registry[$key]="$pts"
    recompute_scores
    log_score_entry "Recorded $key (+$pts). TOTAL=${current_total_score}/100"
    prompt_line_with_ticking_status "Recorded $key (+$pts). TOTAL=${current_total_score}/100 ($(pass_indicator)). Press ENTER... " >/dev/null
  done
}

get_start_epoch_from_hm() {
  local hm="$1"
  if [[ ! "$hm" =~ ^([01][0-9]|2[0-3]):[0-5][0-9]$ ]]; then
    printf "%s" "$(date +%s)"
    return 0
  fi
  local today start_epoch now
  today="$(date +%F)"
  start_epoch="$(date -d "${today} ${hm}" +%s 2>/dev/null || date +%s)"
  now="$(date +%s)"
  if (( start_epoch <= now )); then
    start_epoch="$(date -d "${today} ${hm} tomorrow" +%s 2>/dev/null || date +%s)"
  fi
  printf "%s" "$start_epoch"
}

countdown_to_start() {
  local start_epoch="$1"
  while true; do
    local now remaining
    now="$(date +%s)"
    remaining=$((start_epoch - now))
    if (( remaining <= 0 )); then
      printf "\n=== EXAM STARTED ===\n" >"$controlling_terminal"
      beep
      break
    fi
    printf "\rExam begins in: %s  " "$(format_time_hms "$remaining")" >"$controlling_terminal"
    sleep 1
  done
  printf "\n" >"$controlling_terminal"
}

update_terminal_size
clear_screen
show_cursor

printf "Enter exam start time (HH:MM, 24-hour): " >"$controlling_terminal"
IFS= read -r start_hm <"$controlling_terminal" || start_hm=""
exam_start_epoch="$(get_start_epoch_from_hm "$start_hm")"
exam_end_epoch=$((exam_start_epoch + (23*3600) + (45*60)))

printf "\nWaiting for exam start...\n" >"$controlling_terminal"
countdown_to_start "$exam_start_epoch"

next_break_epoch=$((exam_start_epoch + break_interval_seconds))
next_reassessment_epoch=$((exam_start_epoch + reassessment_interval_seconds))

scheduled_nap_epochs=()
for off in "${nap_offset_schedule[@]}"; do
  scheduled_nap_epochs+=( $((exam_start_epoch + off)) )
done

recompute_scores
hide_cursor

while true; do
  stage_cancel_requested=0
  current_ui_mode="MENU"
  current_stage_name="menu"
  current_stage_seconds_remaining=-1
  last_rendered_status_snapshot=""
  print_menu

  sel="$(prompt_line_with_ticking_status "CMD> ")"
  [[ $forced_interrupt -eq 1 ]] && continue

  case "${sel,,}" in
    1) run_stage "Recon" 25 0; doc_checkpoint_loop "Recon" ;;
    2) run_stage "Exploitation Attempt" 45 1; doc_checkpoint_loop "Exploitation Attempt" ;;
    3) run_stage "Linux PrivEsc Funnel" 20 1; doc_checkpoint_loop "Linux PrivEsc Funnel" ;;
    4) run_stage "Windows PrivEsc Funnel" 30 1; doc_checkpoint_loop "Windows PrivEsc Funnel" ;;
    5) run_stage "Gap Review" 10 1; doc_checkpoint_loop "Gap Review" ;;
    6) run_stage "Documentation Sprint" 15 1 ;;
    7) run_stage "Manual Break" 5 0 ;;
    8) run_stage "Manual Nap" 120 0 ;;
    9) score_menu ;;
    \?) print_help; prompt_line_with_ticking_status "Press ENTER... " >/dev/null ;;
    0)
      confirm="$(prompt_line_with_ticking_status "Type ${EXIT_PHRASE} to quit: ")"
      if [[ "$confirm" == "$EXIT_PHRASE" ]]; then
        clear_screen
        show_cursor
        printf "%s\n" "Exiting deliberately." >"$controlling_terminal"
        exit 0
      fi
      ;;
    *) ;;
  esac
done