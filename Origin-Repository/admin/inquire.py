from flask import Response,request,Blueprint
from admin.pool import pool
from mysql.connector import errors
import json

inquire=Blueprint('inquire', __name__)

@inquire.route("/api/attractions")
def searchViewpointAll():
	try:
		keyword=request.args.get("keyword")
		page=request.args.get("page")
		db = pool.get_connection()
		cursor = db.cursor(dictionary=True)

		# LIMIT範圍，p2多1，確定有沒有下一頁
		if page!=None:
			p=int(page)
			if p==0:
				p1=0
				p2=12
			else:
				p1=p*12
				p2=12+(p*12)
		else:
			cursor.execute('SELECT COUNT(id) FROM trip')
			result_Q= cursor.fetchone()
			p1=0
			p2=result_Q['COUNT(id)']
		if keyword!=None:
			sql='SELECT `id`,name,category,description,address,transport,mrt,longitude,latitude,img FROM trip WHERE name LIKE "%s" ORDER BY `id` LIMIT %s,%s'%("%"+keyword+"%",p1,p2)

		else:
			sql="SELECT `id`,name,category,description,address,transport,mrt,longitude,latitude,img FROM trip ORDER BY `id` LIMIT %s,%s"%(p1,p2)
		
		cursor.execute(sql)
		result= cursor.fetchall()

		# 判斷nextPage
		if result!=[]:
			summary=[]
			img=[]
			for i in result:
				imgurl=i["img"].split(' ')
				img=imgurl[0].split(',')
				subsummay={"id":i["id"],"name":i["name"],"category":i["category"],"description":i["description"],"address":i["address"],"transport":i["transport"],"mrt":i["mrt"],"longitude":i["longitude"],"latitude":i["latitude"],"img":img}
				summary.append(subsummay)

				

				# nextPage的設定，沒有超過12比的沒有下一頁
				if len(result)>12 and p2==result_Q['COUNT(id)']:
					nextPage=None
				elif len(result)>12 and p!=None:# for api/attractions
					nextPage=p+1
				else:# for api/attractions沒有大於12，p不是0也不是None，代表沒下一頁
					nextPage=None
				returnText={"nextPage":nextPage,"data":summary}

		else:
			returnText={"error":result==[],"message":"查無資料"}

		data=json.dumps(returnText,ensure_ascii=False)
		db.commit()
		return data
	
	except errors.Error as e:
		print("error",e)
	finally:
		db.close()