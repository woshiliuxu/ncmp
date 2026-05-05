"""云贝签到：POST /weapi/point/dailyTask（与 NeteaseCloudMusicApi 文档「云贝签到」一致）"""

from src.core.signer import Signer


def run_yunbei_signin(session, logger, config) -> None:
    """
    使用与合伙人评分相同的 weapi 加密方式请求云贝签到。
    type 含义：0 为安卓端签到（常见脚本默认）；若与你的账号不符可改为 1（web/PC）。
    """
    try:
        signer = Signer(session, "", logger, config)
        csrf = str(session.cookies["__csrf"])
        data = {"type": 0, "csrf_token": csrf}
        params = {
            "params": signer._get_params(data),
            "encSecKey": signer._get_enc_sec_key(),
        }
        url = f"https://music.163.com/weapi/point/dailyTask?csrf_token={csrf}"
        response = session.post(
            url,
            data=params,
            cookies={"os": "android"},
            headers={"Referer": "https://music.163.com/"},
        ).json()

        code = response.get("code")
        msg = response.get("msg") or response.get("message") or ""

        if code == 200:
            logger.info("云贝签到成功")
            return

        already_hint = ("重复", "已经", "已完成", "请勿")
        if msg and any(k in msg for k in already_hint):
            logger.info(f"云贝签到：{msg}")
            return

        logger.warning(f"云贝签到未成功: code={code}, msg={msg}")
    except Exception as e:
        logger.warning(f"云贝签到异常（不影响合伙人任务）: {e}")
