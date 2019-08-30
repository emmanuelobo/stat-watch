import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { ProfileComponent } from './profile/profile.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { DataService } from './services/data.service';
import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { CompareComponent } from './compare/compare.component';
import { NewsComponent } from './news/news.component';
import { LeagueLeadersComponent } from './league-leaders/league-leaders.component';
import { HomeComponent } from './home/home.component';
import { RoutingModule } from './routing.module';

@NgModule({
  declarations: [
    AppComponent,
    ProfileComponent,
    AnalyticsComponent,
    LoginComponent,
    RegisterComponent,
    CompareComponent,
    NewsComponent,
    LeagueLeadersComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RoutingModule
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
