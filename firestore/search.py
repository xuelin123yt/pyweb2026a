import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔍 讓使用者輸入關鍵字
keyword = input("請輸入老師名字關鍵字：")

collection_ref = db.collection("靜宜資管")
docs = collection_ref.get()

found = False

for doc in docs:
    data = doc.to_dict()
    teacher = data.get("name", "")
    lab = data.get("lab", "")

    if keyword in teacher:
        print(f"老師：{teacher}，研究室：{lab}")
        found = True

if not found:
    print("查無資料")