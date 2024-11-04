# This API is responsible for fetching data from the server to the app.

from flask import Flask, request, jsonify, current_app, make_response
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from json import dumps
from datetime import date, datetime
import base64, os, json, heapq

def objToStr(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime('%Y-%m-%d / %H:%M:%S')
    elif obj is None:
        return None
    return obj


def dateToStr(date):
    return date.strftime("%Y-%m-%d")

def strToDate(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    return None

def get_data(param):  # param: {}
    session = current_app.db_session()
    content = param["Content"]
    data_list = {}
    if content == "x" or content == "insta":  # x, insta용 처리문
        startDate, endDate = param.get("startDate"), param.get("endDate")
        try:
            results = session.execute(text("""
            SELECT * FROM x_db 
            WHERE DATE(event_date) BETWEEN :startDate AND :endDate
            """), {'startDate': startDate, 'endDate': endDate})

            for idx, result in enumerate(results):
                photo_paths = result[9].split(",") if result[9] else []
                photo_data = []

                for photo_path in photo_paths:
                    full_path = os.path.join("/home/ec2-user/profile_main", photo_path)
                    try:
                        with open(full_path, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            photo_data.append(encoded_string)
                    except FileNotFoundError:
                        pass

                if dateToStr(result[6]) in data_list:
                    data_list[dateToStr(result[6])].append({
                        "sns": "x",
                        "kind": objToStr(result[1]),
                        "title": objToStr(result[2]),
                        "detail": objToStr(result[3]),
                        "artist": objToStr(result[4]),
                        "id": objToStr(result[5]),
                        "event_date": objToStr(result[6]),
                        "post_date": objToStr(result[7]),
                        "url": objToStr(result[8]),
                        "photos": photo_data
                    })
                else:
                    data_list[dateToStr(result[6])] = [{
                        "sns": "x",
                        "kind": objToStr(result[1]),
                        "title": objToStr(result[2]),
                        "detail": objToStr(result[3]),
                        "artist": objToStr(result[4]),
                        "id": objToStr(result[5]),
                        "event_date": objToStr(result[6]),
                        "post_date": objToStr(result[7]),
                        "url": objToStr(result[8]),
                        "photos": photo_data
                    }]

            return data_list if data_list else {
                "": [{"sns": ""}]
            }
        except:
            return data_list if data_list else {
                "": [{"sns": ""}]
            }
        finally:
            session.close()

    elif content == "bboard":
        if "write" in param:  # 게시판에 데이터를 쓸 때
            try:
                postDate = objToStr(param["post_date"])
                if postDate == None:
                    return {param["nickname"]: False}


                session.execute(text("""
                INSERT INTO bulletin_board (nickname, title, content, post_date, artist)
                VALUES (:nickname, :title, :content, :post_date, :artist);
                """), {
                    "nickname": param["nickname"],
                    "title": param["title"],
                    "content": param["content"],
                    "post_date": postDate,
                    "artist": param["artist"]
                    }
                )
                session.commit()

                return {param["nickname"]: {"_": True}}
            except:
                return {param["nickname"]: {"_": False}}
            finally:
                session.close()

        elif "delete" in param:  # 게시판의 데이터를 지울 때
            try:
                postDate = objToStr(param["post_date"])
                if postDate == None:
                    return {param["nickname"]: {"_": False}}

                #return 하는거 없음
                _ = session.execute(text(""" 
                DELETE FROM bulletin_board
                WHERE nickname = :nickname
                AND title = :title
                AND content = :content
                AND post_date = :post_date
                AND artist = :artist;
                """), {
                    "nickname": param["nickname"],
                    "title": param["title"],
                    "content": param["content"],
                    "post_date": postDate,
                    "artist": param["artist"]
                }).fetchall()

                return {param["nickname"]: {"_": True}}


            except:
                return {param["nickname"]: {"_": False}}
            finally:
                session.close()
        else:
            results = []
            if param.get("all"):  # db의 모든 정보를 다 가져오도록 해주는 코드
                results = session.execute(text("""
                SELECT * FROM bulletin_board;
                """)).fetchall()

            elif "nickname" in param:  # id를 처리해주는 코드
                nickname = param["nickname"]
                results = session.execute(text("""
                SELECT * FROM bulletin_board
                WHERE nickname = :nickname;
                """), {"nickname": nickname}).fetchall()

            elif "startDate" in param and "endDate" in param:  # 날짜의 범위를 처리해주는 코드
                startDate, endDate = param["startDate"] + " 00:00:00", param["endDate"] + " 23:59:59"
                results = session.execute(text("""
                SELECT * FROM bulletin_board
                WHERE post_date BETWEEN :start_date AND :end_date;
                """), {"start_date": startDate, "end_date": endDate}).fetchall()

            try:
                data_list = {}
                for idx, value in enumerate(results):
                    data_list[idx] = {
                        "nickname": value[1],
                        "title": value[2],
                        "content": value[3],
                        "post_date": objToStr(value[4]),
                        "artist": value[5],
                        "likes": str(value[6]),
                        "view": str(value[7])
                    }
                return data_list if data_list else {
                    "": {"nickname": ""}
                }
            except:
                return data_list if data_list else {
                    "": {"nickname": ""}
                }
            finally:
                session.close()

    elif content == "cafe":
        results = []
        if param.get("all"):
            results = session.execute(text("""
            SELECT * FROM cafe_db;""")).fetchall()

        elif param.get("startDate") and param.get("endDate"):
            startDate = param["startDate"]
            endDate = param["endDate"]

            results = session.execute(text("""
            SELECT * FROM cafe_db 
            WHERE :startDate <= DATE(start_date) AND DATE(end_date) <= :endDate
            """), {'startDate': startDate, 'endDate': endDate})

        try:
            data_list = []
            for idx, value in enumerate(results):
                data_list.append({
                    "celebrity": value[1],
                    "uploader": value[2],
                    "start_date": dateToStr(value[3]),
                    "end_date": dateToStr(value[4]),
                    "place": value[5],
                    "post_url": value[6],
                    "address": value[7]
                })

            data_list.sort(key=lambda x: (
            (strToDate(x["start_date"]) if x["start_date"] is not None else float('-inf'), 
            x["celebrity"][::-1], 
            len(x["celebrity"]))), reverse=True)

            _data_list = {}
            for idx, value in enumerate(data_list):
                value["num"] = idx
                if value["celebrity"] in _data_list:  # 특정 연예인에 대한 타 생일카페 정보가 존재함
                    _data_list[value["celebrity"]].append(value)
                else:
                    _data_list[value["celebrity"]] = [value]

            data_list = _data_list
            return data_list if data_list else {
                "": [{"celebrity": ""}]
            }
        except:
            return data_list if data_list else {
                "": [{"celebrity": ""}]
            }
        finally:
            session.close()

    elif content == "recentData":
        with open("/home/ec2-user/search_main/tmp.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            data = {key: [value] for key, value in data.items()}
            return data

    elif content == "image":
        IMAGE_DIR = "/home/ec2-user/profile_main/image/artist"

        filename = param.get("filename")
        if filename == None:
            return "Filename parameter is required", 400

        filepath = os.path.join(IMAGE_DIR, filename) + ".jpeg"

        if os.path.exists(filepath):
            with open(filepath, "rb") as imagefile:
                encoded_string = base64.b64encode(imagefile.read()).decode("utf-8")
                return {"_": {"imageData": encoded_string}}

        return "File not found", 404

    return {}
    # 아무것도 해당 안될때


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    engine = create_engine(app.config["DB_URL"], max_overflow=0)
    session_factory = sessionmaker(bind=engine)
    app.db_session = scoped_session(session_factory)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.db_session.remove()

    @app.route("/api_ulti", methods=["POST"])
    def api_main():
        data = request.json
        data = data.get("param")

        if not data:
            return jsonify({"error": "param parameter is required"}), 400

        newdata = get_data(data)
        newdata = dumps(newdata, ensure_ascii=False)
        response = make_response(newdata)
        response.headers["Content-Type"] = "application/json;"
        return response

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
