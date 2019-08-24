import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { ProfileComponent } from './profile/profile.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { DataService } from './services/data.service';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    ProfileComponent,
    AnalyticsComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule

  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
