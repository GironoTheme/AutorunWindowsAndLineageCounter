from Purple.autorun_la_windows import autorun_lineage_windows
# from LA.go_to_world import move_and_click, sleep
from Counter.launch_search import launch_search
from logger import logger

try:
    #sleep(6)
    # move_and_click(888, 466)

    autorun_lineage_windows.launch()

    print('Основной блок скрипта окончен')

except Exception as e:
    print('В основной части кода ошибка \nАварийное включение счетчика')
    logger.error(f'{e}')
    launch_search()

