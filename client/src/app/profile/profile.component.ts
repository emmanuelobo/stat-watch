import { Component, OnInit } from '@angular/core';
import { DataService } from '../services/data.service';
import { PlayerProfile } from '../class/playerprofile.class';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  public player: PlayerProfile;

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.getPlayerProfile().subscribe(data => {
      this.player = new PlayerProfile(data);
    });
  }

}
