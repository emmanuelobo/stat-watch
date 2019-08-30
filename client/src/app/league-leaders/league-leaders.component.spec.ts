import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LeagueLeadersComponent } from './league-leaders.component';

describe('LeagueLeadersComponent', () => {
  let component: LeagueLeadersComponent;
  let fixture: ComponentFixture<LeagueLeadersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LeagueLeadersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LeagueLeadersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
