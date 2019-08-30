import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

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
  ],
  imports: [
    BrowserModule,
    HttpClientModule

  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
