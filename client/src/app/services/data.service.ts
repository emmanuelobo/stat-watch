import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable()
export class DataService {

  constructor(private http: HttpClient) { }

  public getPlayerProfile() {

    return this.http.get('http://localhost:8080/players/32/profile');
  }

  public getPlayerAverages() {

  }

  public getPlayerInformation() {

  }

}
