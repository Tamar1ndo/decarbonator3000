# app/dropbox/client.py
import dropbox
from app.dropbox import env

def get_client() -> dropbox.Dropbox:
    """
    สร้าง Dropbox client จาก access token ใน .env
    """
    dbx = dropbox.Dropbox(env.DROPBOX_TOKEN)
    return dbx
