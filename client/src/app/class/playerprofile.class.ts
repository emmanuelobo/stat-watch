import { PlayerStatistics } from './playerstatistics.class';

export class PlayerProfile {
    firstname: string;
    lastname: string;
    fullname: string;
    dob: string;
    school: string;
    height: string;
    weight: string;
    country: string;
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
    }
}
