import { PlayerStatistics } from './playerstatistics.class';

export class PlayerProfile {
    firstname: string;
    lastname: string;
    fullname: string;
    dob: string;
    school: string;
    height: string;
    weight: string;
    nationality: string;
    experience: number;
    jersey: number;
    profilepicture: string;
    team: string;
    stats: PlayerStatistics;
    constructor(data: Object) {
        this.firstname = data['player']['FIRST_NAME'];
        this.lastname = data['player']['LAST_NAME'];
        this.fullname = data['player']['DISPLAY_FIRST_LAST'];
        this.dob = data['player']['BIRTHDATE'].slice(5);
        this.stats = new PlayerStatistics(data['stats']['PTS'], data['stats']['AST'], data['stats']['REB']);
        this.weight = data['player']['WEIGHT'];
        this.height = data['player']['HEIGHT'];
        this.school = data['player']['SCHOOL'];
        this.nationality = data['player']['COUNTRY'];
        this.experience = data['player']['SEASON_EXP'];
        this.jersey = data['player']['JERSEY'];
        this.team = data['player']['TEAM_NAME'];
        this.profilepicture = data['profile_pic'];
    }
}
