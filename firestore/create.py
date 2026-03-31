import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc = {
  "name": "王奕翔",
  "mail": "xuelin123yt@gmail.com",
  "lab": 579
}

doc_ref = db.collection("靜宜資管").document("WANG YI-SIANG")
doc_ref.set(doc)