from module.base.timer import Timer
from module.logger import logger
from module.ui.page import *


def game(self, skip_first_screenshot=True):
    logger.info('Open event mini game')
    click_timer = Timer(0.3)

    # 游戏start
    while 1:
        if skip_first_screenshot:
            skip_first_screenshot = False
        else:
            self.device.screenshot()

        # 点击开始
        if click_timer.reached() and self.appear_then_click(self.event_assets.MINI_GAME_START, offset=10, interval=2):
            logger.info('Start event mini game')
            click_timer.reset()
            continue

        if self.appear(self.event_assets.MINI_GAME_CLICK, offset=10):
            break

    while 0:
        self.device.screenshot()

        if self.appear(self.event_assets.MINI_GAME_START, offset=10):
            break

        # 结束
        if click_timer.reached() and self.appear_then_click(self.event_assets.MINI_GAME_BACK, offset=10, interval=2):
            logger.info('Event mini game done')
            self.device.sleep(3)
            click_timer.reset()
            continue

        # 技能1
        if (
            click_timer.reached()
            and self.appear(self.event_assets.MINI_GAME_TIME_OUT, offset=10)
            and self.appear_then_click(self.event_assets.MINI_GAME_SKILL1, offset=10, interval=10)
        ):
            click_timer.reset()
            continue

        # 技能2
        if (
            click_timer.reached()
            and self.appear(self.event_assets.MINI_GAME_TIME_OUT, offset=10)
            and self.appear_then_click(self.event_assets.MINI_GAME_SKILL2, offset=10, interval=10)
        ):
            click_timer.reset()
            continue

        # 循环点击
        if self.appear(self.event_assets.MINI_GAME_CLICK, offset=10):
            self.device.click_minitouch(360, 1000)
            self.device.sleep(0.5)
            continue

        # 关闭窗口
        if click_timer.reached() and self.appear_then_click(
            self.event_assets.MINI_GAME_CLOSE, offset=10, interval=1, static=False
        ):
            click_timer.reset()
            continue

    # 领取奖励
    while 1:
        self.device.screenshot()

        if (
            click_timer.reached()
            and self.appear(self.event_assets.MINI_GAME_START, offset=10)
            and self.appear(self.event_assets.MINI_GAME_REWARD_DONE, offset=10)
        ):
            break

        if (
            click_timer.reached()
            and self.appear(self.event_assets.MINI_GAME_START, offset=10)
            and self.appear_then_click(self.event_assets.MINI_GAME_REWARD, offset=10, interval=1)
        ):
            click_timer.reset()
            continue

        # 点击领取
        if click_timer.reached() and self.appear_then_click(
            self.event_assets.RECEIVE, offset=10, interval=1, static=False
        ):
            logger.info('Event mini game receive')
            click_timer.reset()
            continue

    # 回到活动主页
    while 1:
        self.device.screenshot()

        if self.appear(self.event_assets.EVENT_CHECK, offset=(30, 30)):
            break

        if click_timer.reached() and self.appear_then_click(GOTO_BACK, offset=10, interval=2):
            click_timer.reset()
            continue

        if click_timer.reached() and self.appear_then_click(
            self.event_assets.MINI_GAME_BACK_CONFIRM, offset=10, interval=2
        ):
            click_timer.reset()
            continue
