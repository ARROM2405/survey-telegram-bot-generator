from datetime import datetime

telegram_update_mock = {
    "update_id": 1,
    "message": {
        "message_id": 2,
        "from": {
            "id": 3,
            "first_name": "Fname",
        },
        "chat": {"id": 4},
        "text": "some text",
        "date": int(
            datetime(2020, 1, 1).timestamp(),
        ),
    },
}
