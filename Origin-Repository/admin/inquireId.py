from flask import Response,request,Blueprint
from admin.pool import pool
from mysql.connector import errors
import json

inquireId=Blueprint('inquireId', __name__)


@inquireId.route("/api/attraction/<n>")
def searchViewpointById(n):
	try:
		db = pool.get_connection()
		cursor = db.cursor(dictionary=True)
		sql="SELECT `id`,name,category,description,address,transport,mrt,longitude,latitude,img FROM attractions WHERE id='%s'"%(n)
		cursor.execute(sql)
		result = cursor.fetchall()
		img=[]
		if cursor!=None:
			u=result[0]["img"].split(',')
			for photo in u:
				img.append(photo)
			m={"data":{"id":result[0]["id"],"name":result[0]["name"],"category":result[0]["category"],"description":result[0]["description"],"address":result[0]["address"],"transport":result[0]["transport"],"mrt":result[0]["mrt"],"longitude":result[0]["longitude"],"latitude":result[0]["latitude"],"img":img}}
			data=json.dumps(m,ensure_ascii=False)
			db.commit()
			return data
		else:
			r={"error":result==None,"message":"景點編號不正確"}
			data=json.dumps(r,ensure_ascii=False)
			return Response(response=data, status=400)
	except errors.Error as e:
		print("Error",e)
	finally:
		db.close()