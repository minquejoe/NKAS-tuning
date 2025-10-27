from datetime import datetime, timedelta, timezone
from functools import cached_property

from module.base.timer import Timer
from module.daemon.assets import *
from module.episode_viewing.assets import *
from module.logger import logger
from module.ui.assets import EPISODE_VIEWING_CHECK, SKIP
from module.ui.page import page_episode_viewing
from module.ui.ui import UI


class EpisodeViewing(UI):
    @cached_property
    def next_tuesday(self) -> datetime:
        """计算下一个周二的时间（北京时间早上4点）"""
        local_now = datetime.now()
        remain = (1 - local_now.weekday()) % 7
        remain = remain + 7 if remain == 0 else remain
        diff = datetime.now(timezone.utc).astimezone().utcoffset() - timedelta(hours=8)
        return local_now.replace(hour=4, minute=0, second=0, microsecond=0) + timedelta(days=remain) + diff

    def view(self):
        # 鉴赏是否完成
        if self.appear(INCOMPLETE, offset=10):
            # 所有花絮，直接点击第一个
            episodes = TEMPLATE_EPISODE.match_multi(self.device.image)

            if len(episodes) > 0:
                while 1:
                    self.device.screenshot()

                    if self.appear(INCOMPLETE, offset=10):
                        self.device.click(episodes[0])
                        self.device.sleep(1)
                    else:
                        break
        self.play()

        logger.info('View done')

    def play(self):
        logger.info('Start view')
        confirm_timer = Timer(1, count=3)
        click_timer = Timer(0.3)

        while 1:
            self.device.screenshot()

            # SKIP
            if click_timer.reached() and self.appear_then_click(SKIP, offset=10, interval=1):
                click_timer.reset()
                continue

            # 领取
            if click_timer.reached() and self.appear_then_click(REWARD, offset=10, interval=1):
                click_timer.reset()
                continue
            if self.handle_reward(interval=1):
                click_timer.reset()
                continue

            # 回到鉴赏页面
            if self.appear(EPISODE_VIEWING_CHECK, offset=10) and self.appear(COMPLETE, offset=10):
                break

            # 下一个花絮超过1秒
            if self.appear(PLAY_HIGHLIGHTS, offset=30):
                if not confirm_timer.started():
                    confirm_timer.start()
                if confirm_timer.reached() and self.appear_then_click(PLAY_HIGHLIGHTS, offset=30, interval=1):
                    continue
            else:
                confirm_timer.clear()

    def run(self):
        logger.hr('Episode Viewing', 1)
        self.ui_ensure(page_episode_viewing, confirm_wait=1)

        try:
            self.view()
        except Exception as e:
            logger.error(e)

        self.config.task_delay(target=self.next_tuesday)
