from Purple.autorun_la_windows import autorun_lineage_windows
from LA.go_to_world import move_and_click, sleep
from Counter.launch_search import launch_search

sleep(6)
move_and_click(888, 466)

autorun_lineage_windows.launch()
launch_search()

