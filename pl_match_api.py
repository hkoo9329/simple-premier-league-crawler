from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from db import PL_database
from webCrawling import PL_match_crawler
import logging
app = Flask(__name__)
api = Api(app, version='0.5', title='PL 매치 정보 API', description='프리미어리그 경기 결과, 일정 등을 조회하는 API입니다.')
ns = api.namespace('matchs', description='시즌 전체 경기, 팀별 경기, 최근 경기 조회')
db = PL_database.Database()
crawler = PL_match_crawler.PL_match_crawler()


model_matchs = api.model('row_match', {
    'id': fields.Integer(readOnly=True, required=True, description='매치 id', help='매치 id 필수'),
    'match_day': fields.String(readOnly=True, required=True, description='경기 날짜', help='경기 날짜 필수'),
    'left_team': fields.String(readOnly=True, required=True, description='왼쪽 팀', help='왼쪽 팀 필수'),
    'right_team': fields.String(readOnly=True, required=True, description='오른쪽 팀', help='오른쪽 팀 필수'),
    'score': fields.String(readOnly=True, required=True, description='스코어')
})
recencySql = """select * from (
            select * from pl_match_db where match_day < NOW()
            order by match_day desc
            limit 3
        )CNT union (
            select * from pl_match_db where match_day >= NOW()
            limit 5
        ) order by id;"""

recencyTeamSql = """select * from (
    select * from pl_match_db
    where match_day < NOW() and (left_team = '{match_team}' or right_team = '{match_team}')
    order by match_day desc
    limit 3
)CNT union (
    select * from pl_match_db
    where match_day >= NOW() and (left_team = '{match_team}' or right_team = '{match_team}')
    limit 5
) order by id;"""


class MatchDAO(object):
    '''프리미어리그 매치 Data Access Object'''
    def __init__(self):
        self.db = db = PL_database.Database()
    
    # 전체 경기를 출력
    def getMatchAll(self):
        rows = db.executeAll("select * from pl_match_db")
        return rows
    
    # 특정 팀의 전체 경기를 출력
    def getMatchByTeamAll(self, team):
        teamNameCheck = self.db.executeOne(
            "select exists (select * from pl_match_db where left_team='{match_team}')as is_empty".format(match_team=team))
        if teamNameCheck['is_empty'] == 1:
            rows = db.executeAll(
                "select * from pl_match_db where left_team = '{match_team}' or right_team = '{match_team}'".format(match_team=team))
            return rows
        else:
            api.abort(404, "{} doesn't exist".format(team))
    
    # 최근 8경기를 출력
    def getMatchRecency(self):
        rows = self.db.executeAll(recencySql)
        return rows

    # 특정 팀의 최근 8경기를 출력
    def getMatchRecencyTeam(self, team):
        log.info(team)
        teamNameCheck = self.db.executeOne(
            "select exists (select * from pl_match_db where left_team='{}') as is_empty".format(team))
        if teamNameCheck['is_empty'] == 1:
            rows = self.db.executeAll(recencyTeamSql.format(match_team=team))
            return rows
        else:
            api.abort(404, "{} doesn't exist".format(team))



DAO = MatchDAO()


@ns.route('/all')
class PLMatchListAll(Resource):
    @ns.marshal_list_with(model_matchs)
    def get(self):
        '''전체 리스트 조회'''
        match_all_list = DAO.getMatchAll()
        log.debug(match_all_list)
        return match_all_list


@ns.route('/all/<string:team>')
@ns.response(404, '해당 팀을 찾을 수 없습니다.')
@ns.param('team', '팀 검색')
class MatchTeamAll(Resource):
    @ns.marshal_list_with(model_matchs)
    def get(self, team):
        '''해당 팀의 모든 경기를 조회'''
        team_all_list=DAO.getMatchByTeamAll(team)
        log.debug(team_all_list)
        return team_all_list


@ns.route('/recency')
class MatchRecency(Resource):
    @ns.marshal_list_with(model_matchs)
    def get(self):
        '''최근 8경기를 조회'''
        recente_match_list = DAO.getMatchRecency()
        log.debug("최근 경기 리스트 : "+recente_match_list)
        return recente_match_list


@ns.route('/recency/<string:team>')
@ns.response(404, '해당 팀을 찾을 수 없습니다.')
@ns.param('team', '팀 검색')
class MatchRecencyTeam(Resource):
    @ns.marshal_list_with(model_matchs)
    def get(self, team):
        '''해당 팀의 최근 8경기를 조회'''
        recente_team_list = DAO.getMatchRecencyTeam(team)
        log.debug("최근 팀 경기 리스트 : "+recente_team_list)
        return  recente_team_list


