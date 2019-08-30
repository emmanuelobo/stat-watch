import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProfileComponent } from './profile/profile.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { HomeComponent } from './home/home.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { LeagueLeadersComponent } from './league-leaders/league-leaders.component';
import { NewsComponent } from './news/news.component';

const appRoutes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: 'news', component: NewsComponent },
    { path: 'league-leaders', component: LeagueLeadersComponent },
    { path: 'players/:id/profile/', component: ProfileComponent },
    { path: 'players/:id/analytics/', component: AnalyticsComponent },
  ];

  @NgModule({
    imports: [
      RouterModule.forRoot(
        appRoutes,
        { enableTracing: true } // <-- debugging purposes only
      )
      // other imports here
    ],
    exports: [
      RouterModule
    ]
  })
export class RoutingModule { }
