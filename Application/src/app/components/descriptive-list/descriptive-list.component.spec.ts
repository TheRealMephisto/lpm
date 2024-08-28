import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DescriptiveListComponent } from './descriptive-list.component';

describe('DescriptiveListComponent', () => {
  let component: DescriptiveListComponent;
  let fixture: ComponentFixture<DescriptiveListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DescriptiveListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DescriptiveListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
