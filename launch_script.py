from Purple.autorun_lineage_windows import autorun_lineage_windows
from Purple.purple import PurpleSingleton
from LineageCounter.launch_search import launch_search

purple_instance = PurpleSingleton.get_instance()
purple_instance.launch_purple()

autorun_lineage_windows.launch()
launch_search()

