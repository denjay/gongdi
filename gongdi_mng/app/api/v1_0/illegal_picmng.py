########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.175898
########################################
from app import auth, p
from app.models import *
from flask import current_app,send_file
from PIL import Image
import os
@auth.valid_login
@p.check("illegal_pic",["view"])
def illegal_pics_id_get(id,jwt = None) -> str:
    data = Illegal_pic.query.filter_by(id=id).first_or_404()
    return send_file(data.save_file_name,mimetype='image/jpeg')
@auth.valid_login
@p.check("illegal_pic",["delete"])
def illegal_pics_id_delete(id,jwt = None) -> str:
    try:
        ill_pic = Illegal_pic.query.filter(Illegal_pic.id == id).first()
        try:
            os.remove(ill_pic.save_file_name)
        except Exception as e:
            pass
        db.session.delete(ill_pic)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("illegal_pic",["insert"])
def illegal_pics_post(pic,illegalid,jwt = None) -> str:
    def get_rate(ws,wd,hs,hd):
        if ws < wd or hs < hd:
            return 1
        # 调整比率，取最大的比率
        rw = ws / wd
        rh = hs / hd
        return max(rw,rh)
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],'illegal')
        os.makedirs(file_path,exist_ok=True)
        # 真实存储的文件增加秒数，防止被覆盖
        file_name = os.path.join(file_path,'%s_%s.%s'%(pic.filename.rsplit('.',1)[0],
                                                       datetime.now().strftime('%Y%m%d%H%M%S'),
                                                       pic.filename.rsplit('.',1)[1]))
        pil_image = Image.open(pic.stream)
        w,h = pil_image.size
        res_rate = get_rate(w, 500, h, 450)
        pil_image.thumbnail((round(w / res_rate), round(h / res_rate)))
        pil_image.save(file_name, 'jpeg')
        data = Illegal_pic(file_name=pic.filename,
                           pic_size=round(os.path.getsize(file_name)/1024,2),
                           save_file_name=file_name,
                           illegalid=illegalid)
        db.session.add(data)
        db.session.commit()
        return data.to_json(), \
               201, {"content-type": "chatset=utf8"}
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_pic",["view"])
def illegal_id_pics_get(id,jwt = None) -> str:
    datas = Illegal_pic.query.filter(Illegal_pic.illegalid==id).all()
    return [data.to_json() for data in datas] ,\
            200 ,{"content-type": "chatset=utf8"}
